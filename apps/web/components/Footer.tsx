export default function Footer() {
  return (
    <footer className="flex justify-center items-center gap-1 text-sm text-muted-foreground py-4">
      <span>Built by</span>
      <a
        href="https://github.com/saptarshiroy39"
        target="_blank"
        rel="noopener noreferrer"
        className="underline"
      >
        Saptarshi Roy
      </a>
      <span>&</span>
      <a
        href="https://github.com/itskdhere"
        target="_blank"
        rel="noopener noreferrer"
        className="underline"
      >
        Krishnendu Das
      </a>
    </footer>
  );
}
