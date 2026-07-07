#!/usr/bin/env bash
# Store Jira API credentials locally (never commit this file).
set -euo pipefail

ENV_DIR="${HOME}/.config/pd-os"
ENV_FILE="${ENV_DIR}/env"

mkdir -p "$ENV_DIR"

if [[ -f "$ENV_FILE" ]] && grep -q '^export JIRA_API_TOKEN=' "$ENV_FILE" 2>/dev/null; then
  echo "Jira credentials already exist in ${ENV_FILE}"
  read -r -p "Overwrite JIRA_EMAIL and JIRA_API_TOKEN? [y/N] " ans
  [[ "${ans,,}" == "y" ]] || exit 0
  # Remove old Jira lines
  grep -v '^export JIRA_' "$ENV_FILE" > "${ENV_FILE}.tmp" || true
  mv "${ENV_FILE}.tmp" "$ENV_FILE"
fi

echo ""
echo "Mozilla Jira uses an API token (not your SSO password in scripts)."
echo "Create one: https://id.atlassian.com/manage-profile/security/api-tokens"
echo ""

read -r -p "Mozilla email (JIRA_EMAIL): " email
read -r -s -p "Atlassian API token (hidden): " token
echo ""

# Trim accidental spaces/newlines from paste
token="$(printf '%s' "$token" | tr -d '[:space:]')"
email="$(printf '%s' "$email" | tr -d '[:space:]')"

if [[ -z "$email" || -z "$token" ]]; then
  echo "Email and token are required." >&2
  exit 1
fi

if [[ ${#token} -lt 16 || ${#token} -gt 80 ]]; then
  echo ""
  echo "⚠  Token length is ${#token} characters — that does not look like an Atlassian API token."
  echo "   API tokens are usually one short line (~24 characters), shown once after you click"
  echo "   \"Create API token\" at:"
  echo "   https://id.atlassian.com/manage-profile/security/api-tokens"
  echo ""
  echo "   Common mistakes: pasting a URL, JWT, cookie, or multiple lines from 1Password."
  read -r -p "Save anyway? [y/N] " badlen
  [[ "${badlen,,}" == "y" ]] || exit 1
fi

{
  echo ""
  echo "# Jira (mozilla-hub) — added $(date +%Y-%m-%d)"
  echo "export JIRA_EMAIL=\"${email}\""
  echo "export JIRA_API_TOKEN=\"${token}\""
} >> "$ENV_FILE"

chmod 600 "$ENV_FILE"
echo ""
echo "Saved to ${ENV_FILE}"
echo ""
echo "Test connection:"
echo "  source ${ENV_FILE}"
echo "  cd $(cd "$(dirname "$0")/../.." && pwd)"
echo "  python3 -m pd_os.cli jira-auth --project 2026-06-ai-velocity-mandate"
