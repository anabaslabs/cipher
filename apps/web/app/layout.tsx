import { Analytics } from "@vercel/analytics/next";
import { Metadata } from "next";
import { Lexend } from "next/font/google";
import { Providers } from "@/components/providers";
import "@workspace/ui/globals.css";

const lexend = Lexend({
  variable: "--font-lexend",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "Cipher",
  description:
    "Your all-in-one toolkit for Cipher Project. Encrypt, Decrypt, Run Frequency Analysis Attack and Generate Report with ease.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${lexend.variable} font-lexend antialiased `}>
        <Providers>{children}</Providers>
        <Analytics />
      </body>
    </html>
  );
}
