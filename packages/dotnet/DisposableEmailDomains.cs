using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace DisposableEmail
{
    /// <summary>
    /// Known disposable / temporary email domains, embedded from domains.txt.
    /// </summary>
    public static class DisposableEmailDomains
    {
        private static readonly HashSet<string> Set;

        /// <summary>Sorted list of known disposable email domains.</summary>
        public static IReadOnlyList<string> Domains { get; }

        static DisposableEmailDomains()
        {
            var asm = typeof(DisposableEmailDomains).GetTypeInfo().Assembly;
            var list = new List<string>();
            using (var stream = asm.GetManifestResourceStream("domains.txt"))
            {
                if (stream == null)
                    throw new InvalidOperationException("embedded resource domains.txt not found");
                using (var reader = new StreamReader(stream))
                {
                    string? line;
                    while ((line = reader.ReadLine()) != null)
                    {
                        line = line.Trim();
                        if (line.Length > 0)
                            list.Add(line);
                    }
                }
            }
            Domains = list;
            Set = new HashSet<string>(list, StringComparer.OrdinalIgnoreCase);
        }

        /// <summary>
        /// Returns true if the email's domain is a known disposable email domain.
        /// Accepts a full address ("foo@mailinator.com") or a bare domain.
        /// Case-insensitive.
        /// </summary>
        public static bool IsDisposable(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                return false;
            var at = email.LastIndexOf('@');
            var domain = (at >= 0 ? email.Substring(at + 1) : email).Trim();
            return Set.Contains(domain);
        }
    }
}
