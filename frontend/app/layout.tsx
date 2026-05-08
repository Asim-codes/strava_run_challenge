import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Run Challenge",
  description: "A live scoreboard for a friendly running challenge.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <header className="top-nav">
            <Link href="/" className="brand">
              Run Club
            </Link>
            <nav aria-label="Main navigation">
              <Link href="/">Current</Link>
              <Link href="/archive">Archive</Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
