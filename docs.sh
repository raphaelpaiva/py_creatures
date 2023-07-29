#!/bin/sh

DOCS_DIR=docs

mkdir -p $DOCS_DIR
for pkg_dir in 'core' 'app'; do
  output_dir="$DOCS_DIR/$pkg_dir"
  mkdir -p "$output_dir"
  pyreverse -ASmy -o svg --colorized -d "$output_dir" "$pkg_dir"
done
