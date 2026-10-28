#!/bin/sh
# Cloudflare Pages build step: copies only the public site into dist/ (keeps _src and the repo internals private).
set -e
rm -rf dist && mkdir dist
for f in *; do
  case "$f" in _src|dist|functions|node_modules) ;; *) cp -r "$f" dist/ ;; esac
done
# Netlify-only rule (blocked /_src on Netlify) is not needed: _src is not published.
: > dist/_redirects
