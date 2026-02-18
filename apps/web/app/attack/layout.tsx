import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Frequency Analysis Attack | CNS Solver",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
