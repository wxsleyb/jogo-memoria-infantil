#!/usr/bin/env python3
"""Curadoria offline de ilustrações da Pixabay API (sem revelar a chave no navegador).

Requer Python 3.9+, Pillow e PIXABAY_API_KEY no ambiente.
  pip install Pillow
  python tools/importar_pixabay.py buscar --tema animais --consulta 'cute cartoon animal isolated'
  # Analise curadoria/candidatos_animais.json, edite curadoria/selecionadas.json.
  python tools/importar_pixabay.py importar
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / 'curadoria'
CACHE = CUR / 'cache'
API_URL = 'https://pixabay.com/api/'
THEMES = ('animais', 'frutas', 'transportes')


def key():
    value = os.environ.get('PIXABAY_API_KEY', '').strip()
    if not value:
        sys.exit('Defina PIXABAY_API_KEY no ambiente antes de executar esta ferramenta.')
    return value


def request(url, *, timeout=22):
    req = Request(url, headers={'User-Agent': 'JogoMemoriaCuradoria/1.0 (biblioteca de imagens selecionadas)', 'Accept':'application/json,image/*'})
    with urlopen(req, timeout=timeout) as r:
        return r.read()


def pixabay_api(params):
    # Nunca gravar chave em arquivos ou em logs. Cache guarda só dados retornados.
    params = {**params, 'key': key()}
    cache_params = {k:v for k,v in params.items() if k != 'key'}
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_hash = hashlib.sha256(json.dumps(cache_params, sort_keys=True).encode()).hexdigest()[:24]
    cache_path = CACHE / (cache_hash + '.json')
    if cache_path.exists() and time.time()-cache_path.stat().st_mtime < 24*3600:
        return json.loads(cache_path.read_text(encoding='utf-8'))
    try:
        result=json.loads(request(API_URL+'?'+urlencode(params)))
    except Exception as exc:
        raise RuntimeError(f'Pixabay API indisponível: {exc}') from exc
    if not isinstance(result.get('hits'),list):
        raise RuntimeError('A Pixabay não retornou uma lista de imagens. Confira a chave e os limites da API.')
    cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


def buscar(args):
    data=pixabay_api({'q':args.consulta,'image_type':'illustration','safesearch':'true','per_page':args.limite,'lang':'en','order':'popular'})
    candidates=[{'id':h['id'], 'tags':h.get('tags',''), 'autor':h.get('user',''), 'pagina':h.get('pageURL',''), 'tipo':h.get('type',''), 'preview':h.get('previewURL','')}
                for h in data.get('hits',[]) if h.get('type') in ('illustration','vector')]
    CUR.mkdir(parents=True,exist_ok=True)
    dest=CUR/f'candidatos_{args.tema}.json'
    dest.write_text(json.dumps({'consulta':args.consulta,'tema':args.tema,'observacao':'REVISE visualmente todas as imagens antes de aprovar','candidatos':candidates},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(candidates)} candidatos listados em {dest.relative_to(ROOT)}.')
    for h in candidates[:12]: print(f"  {h['id']}: {h['tags']} — {h['pagina']}")
    print('Abra os links, verifique cada imagem e adicione somente IDs aprovados a curadoria/selecionadas.json.')


def validar_selecionadas(data):
    if not isinstance(data,dict):raise ValueError('O arquivo de seleção deve ser um objeto JSON com os temas.')
    out=[];seen=set()
    for theme in THEMES:
        rows=data.get(theme,[])
        if not isinstance(rows,list):raise ValueError(f'Tema {theme} deve conter uma lista.')
        for row in rows:
            if not isinstance(row,dict):raise ValueError('Cada item deve possuir id e nome.')
            id_=row.get('id');name=row.get('nome','')
            if isinstance(id_,bool) or not isinstance(id_,int) or id_<=0 or not isinstance(name,str) or not name.strip() or len(name)>55:
                raise ValueError(f'Item inválido em {theme}: {row}')
            if id_ in seen:raise ValueError(f'ID repetido: {id_}')
            seen.add(id_);out.append((theme,id_,name.strip()))
    return out


def baixar_imagem(url):
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname not in ('pixabay.com','cdn.pixabay.com'):
        raise ValueError('Origem de imagem fora da Pixabay; download cancelado.')
    raw=request(url)
    if len(raw)>12*1024*1024:raise ValueError('Imagem muito grande para importação.')
    source=Image.open(io.BytesIO(raw))
    source.verify() # Verificar integridade antes de decodificar novamente.
    source=Image.open(io.BytesIO(raw)).convert('RGBA')
    source=ImageOps.contain(source, (328,368), Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA', (360,420), '#FFF8F5')
    canvas.alpha_composite(source, ((360-source.width)//2,(390-source.height)//2))
    return canvas.convert('RGB')


def importar(_args):
    selection_file=CUR/'selecionadas.json'
    if not selection_file.exists():raise FileNotFoundError('Edite curadoria/selecionadas.json antes de importar.')
    selections=validar_selecionadas(json.loads(selection_file.read_text(encoding='utf-8')))
    if not selections:
        print('Nenhuma ilustração aprovada ainda. Nada foi alterado. O jogo continua usando as 96 ilustrações locais.');return
    gallery={t:[] for t in THEMES};credits=[]
    for theme,id_,name in selections:
        try:
            data=pixabay_api({'id':id_,'image_type':'illustration','safesearch':'true'})
            hit=next((h for h in data.get('hits',[]) if h.get('id')==id_),None)
            if not hit or hit.get('type') not in ('illustration','vector'):
                raise ValueError('ID não corresponde a uma ilustração autorizada na busca; verifique na Pixabay.')
            image_url=hit.get('webformatURL') or hit.get('largeImageURL')
            if not image_url:raise ValueError('A API não forneceu URL válida.')
            target=ROOT/'img'/'pixabay'/theme/f'{id_}.webp'
            target.parent.mkdir(parents=True,exist_ok=True)
            baixar_imagem(image_url).save(target,'WEBP',quality=90,method=6)
            page=hit.get('pageURL','')
            gallery[theme].append({'nome':name,'src':f'img/pixabay/{theme}/{id_}.webp','pagina':page,'autor':hit.get('user',''),'origem':'Pixabay'})
            credits.append((theme,name,page,hit.get('user','')))
            print('Importado:',theme,name,id_)
        except Exception as exc:
            print(f'Não foi possível importar {id_} ({name}): {exc}',file=sys.stderr)
    out=ROOT/'biblioteca-pixabay.js'
    out.write_text('// Imagens da Pixabay aprovadas e salvas localmente.\nwindow.BIBLIOTECA_PIXABAY = '+json.dumps(gallery,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    md=['# Créditos das ilustrações importadas da Pixabay','',f'Atualizado em {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}.','', 'Imagens revisadas manualmente antes de entrar no jogo. Consulte as condições de uso da Pixabay.','']
    md += [f'- **{theme} — {name}**: {page} (autor: {autor or "não informado"})' for theme,name,page,autor in credits]
    (ROOT/'CREDITOS_PIXABAY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(f'Concluído: {sum(map(len,gallery.values()))} arquivos importados. O jogo pode continuar offline.')


def main():
    p=argparse.ArgumentParser(description='Buscar e importar ilustrações aprovadas usando Pixabay API')
    sub=p.add_subparsers(dest='comando',required=True)
    b=sub.add_parser('buscar',help='Pesquisar candidatos; não adiciona imagens ao jogo automaticamente')
    b.add_argument('--tema',required=True,choices=THEMES)
    b.add_argument('--consulta',required=True,help='Busca em inglês, ex.: cute cartoon apple isolated')
    b.add_argument('--limite',type=int,default=40,choices=range(3,201),metavar='3-200')
    sub.add_parser('importar',help='Baixar as imagens aprovadas em selecionadas.json e atualizar a biblioteca')
    args=p.parse_args()
    try:
        if args.comando=='buscar':buscar(args)
        else:importar(args)
    except Exception as exc:sys.exit(f'Erro: {exc}')

if __name__=='__main__':main()
