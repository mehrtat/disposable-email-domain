# DisposableEmailDomain

A large, **auto-updated** list of disposable / temporary / throwaway email domains (mailinator, 10minutemail, guerrillamail, …), with a tiny zero-dependency `IsDisposable()` helper for .NET.

- **160,000+ domains**, aggregated from 6 well-maintained public blocklists, deduped and normalized (lowercased, IDNA/punycode).
- **Refreshed daily** — a new version is published only when the set actually changes.
- **netstandard2.0**, zero dependencies. The list is embedded, lookups are O(1).

## Install

```bash
dotnet add package DisposableEmailDomain
```

## Usage

```csharp
using DisposableEmail;

DisposableEmailDomains.IsDisposable("someone@mailinator.com"); // true
DisposableEmailDomains.IsDisposable("someone@gmail.com");      // false
DisposableEmailDomains.IsDisposable("mailinator.com");         // true (bare domain also works)

DisposableEmailDomains.Domains.Count; // 160000+  — the full list if you want it
```

`IsDisposable(input)` accepts a full email (`user@domain`) or a bare domain, is case-insensitive, and returns `bool`.

## Why

Blocking disposable-email signups cuts fraud, fake accounts, and junk. Hand-maintaining such a list is a losing battle — this package keeps it fresh for you automatically.

## Data sources

Aggregated + deduped from `disposable/disposable-email-domains`, `ivolo/disposable-email-domains`, `FGRibreau/mailchecker`, `wesbos/burner-email-providers`, `disposable-email-domains/disposable-email-domains`, and `7c/fakefilter`. Credit to their maintainers.

## Also available for

Go — `go get github.com/mehrtat/disposable-email-domain` · npm — `npm install disposable-email-domain`

Source, issues, and how to contribute a source: **https://github.com/mehrtat/disposable-email-domain**

## License

MIT © Mehrdad TAT
