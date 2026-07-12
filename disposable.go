// Package disposable provides the aggregated list of known disposable /
// temporary email domains, embedded at build time from domains.txt.
//
//	import disposable "github.com/mehrtat/disposable-email-domain"
//	disposable.IsDisposable("foo@mailinator.com") // true
package disposable

import (
	_ "embed"
	"strings"
)

//go:embed domains.txt
var raw string

// Domains is the sorted list of known disposable email domains.
var Domains = strings.Split(strings.TrimSpace(raw), "\n")

var domainSet = func() map[string]struct{} {
	m := make(map[string]struct{}, len(Domains))
	for _, d := range Domains {
		if d != "" {
			m[d] = struct{}{}
		}
	}
	return m
}()

// IsDisposable reports whether the domain part of email is a known disposable
// email domain. The comparison is case-insensitive. A bare domain (no "@") is
// checked directly.
func IsDisposable(email string) bool {
	domain := email
	if at := strings.LastIndex(email, "@"); at != -1 {
		domain = email[at+1:]
	}
	domain = strings.ToLower(strings.TrimSpace(domain))
	_, ok := domainSet[domain]
	return ok
}
