import { readFileSync } from "fs";
import { join } from "path";

// domains.json is shipped alongside the package (see package.json "files").
// At runtime dist/index.js sits in dist/, so the list is one level up.
const domainsData: string[] = JSON.parse(
  readFileSync(join(__dirname, "..", "domains.json"), "utf8")
);

/** Sorted list of known disposable / temporary email domains. */
export const domains: readonly string[] = domainsData;

const domainSet = new Set(domainsData);

/**
 * Returns true if the email's domain is a known disposable email domain.
 * Accepts a full address ("foo@mailinator.com") or a bare domain
 * ("mailinator.com"). Case-insensitive.
 */
export function isDisposable(email: string): boolean {
  const at = email.lastIndexOf("@");
  const domain = (at === -1 ? email : email.slice(at + 1)).trim().toLowerCase();
  return domainSet.has(domain);
}

export default { domains, isDisposable };
