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
  title: "CNS Solver",
  description: "CNS Solver",
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
      </body>
    </html>
  );
}
