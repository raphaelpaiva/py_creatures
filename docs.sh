#!/bin/sh

set -e

GREEN='\033[0;32m'
BOLD_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

SCRIPT_NAME=$0
LOG_PREF="${SCRIPT_NAME}"

DOCS_DIR=docs
DIAGRAMS_DIR="${DOCS_DIR}/diagrams"

log_info() {
  echo "${BOLD_GREEN}${LOG_PREF} [INFO]: ${GREEN}$1${COLOR_OFF}"
}

log_info "Installing prereqs..."
pip install virtualenv
virtualenv venv
. ./venv/bin/activate

pip install -r requirements-docs.txt

# Generate docs site
log_info "Generating docs site..."
mkdocs build

# Generate class diagrams
log_info "Generating class diagrams..."
mkdir -p $DIAGRAMS_DIR
for pkg_dir in 'creatures/core' 'creatures/app'; do
  output_dir="$DIAGRAMS_DIR/$pkg_dir"
  mkdir -p "$output_dir"
  pyreverse -ASmy -o svg --colorized -d "$output_dir" "$pkg_dir"
done

log_info "Done!"