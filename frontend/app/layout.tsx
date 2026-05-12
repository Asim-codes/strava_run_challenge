import type { Metadata, Viewport } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Run Club",
  description: "A live scoreboard for a friendly running challenge.",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    title: "Run Club",
    statusBarStyle: "black-translucent",
  },
  icons: {
    icon: "/favicon.png",
    apple: "/apple-touch-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#f5f0eb",
  width: "device-width",
  initialScale: 1,
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
              <Link href="/badges">Badges</Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
