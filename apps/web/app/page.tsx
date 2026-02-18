import Link from "next/link";
import Header from "@/components/Header";
import { Button } from "@workspace/ui/components/button";

export default function Home() {
  return (
    <>
      <Header />
      <main className="flex flex-col justify-center items-center gap-2 p-6 w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-6xl">
          <Button variant="outline" asChild>
            <Link href="/encrypt">Encrypt</Link>
          </Button>
          <Button variant="outline">
            <Link href="/decrypt">Decrypt</Link>
          </Button>
          <Button variant="outline">
            <Link href="/">Frequency Analysis Attack</Link>
          </Button>
          <Button variant="outline">
            <Link href="/">Generate Report</Link>
          </Button>
        </div>
      </main>
    </>
  );
}
