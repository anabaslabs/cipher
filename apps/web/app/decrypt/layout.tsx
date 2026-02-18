import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Decrypt | Cipher",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
