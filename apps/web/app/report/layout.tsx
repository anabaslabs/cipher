import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Generate Report | Cipher",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
