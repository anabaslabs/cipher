import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Encrypt | CNS Solver",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
