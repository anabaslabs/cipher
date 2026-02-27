"use client";

import axios from "axios";
import { useCallback, useRef, useState } from "react";
import Header from "@/components/Header";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@workspace/ui/components/select";
import { Field, FieldLabel } from "@workspace/ui/components/field";
import { ButtonGroup } from "@workspace/ui/components/button-group";
import { Input } from "@workspace/ui/components/input";
import { Button } from "@workspace/ui/components/button";
import { formatBytes } from "@/hooks/use-file-upload";
import type { State } from "@/components/FileSelector";
import FileSelector from "@/components/FileSelector";
import {
  IconCheck,
  IconClock,
  IconCopy,
  IconDice5,
  IconDownload,
  IconFileInfo,
  IconKey,
  IconLoader,
  IconLock,
  IconReload,
  IconX,
} from "@tabler/icons-react";

type DownloadFile = {
  url: string;
  filename: string;
  size: number;
  label: string;
};

const algoSuffixMap: Record<string, string> = {
  caesar: "_CC",
  permute: "_PC",
  vigenere: "_VC",
  playfair: "_PFC",
  hill: "_HC",
  des: "_DC",
  aes: "_AES",
  rc5: "_RC5",
};

export default function Encrypt() {
  const [state, setState] = useState<State>("idle");
  const [formState, setFormState] = useState({
    file: null as File | null,
    encryptionMethod: null as string | null,
    encryptionKey: null as string | null,
    aesSize: "128",
    rc5W: "32",
    rc5R: 12,
    rc5B: 16,
  });
  const [downloadFiles, setDownloadFiles] = useState<DownloadFile[]>([]);
  const [timeTaken, setTimeTaken] = useState<number | null>(null);
  const [keyCopied, setKeyCopied] = useState(false);
  const [isGeneratingKey, setIsGeneratingKey] = useState(false);
  const clearFilesRef = useRef<(() => void) | null>(null);

  const playSound = () => {
    const audio = new Audio("/enchanting_table.ogg");
    audio.volume = 0.6;
    audio.play().catch(() => {});
  };

  const handleFileChange = useCallback((file: File | null) => {
    setFormState((prev) => ({ ...prev, file }));
  }, []);

  const handleSetClear = useCallback((clearFn: () => void) => {
    clearFilesRef.current = clearFn;
  }, []);

  const handleClear = useCallback(() => {
    downloadFiles.forEach((f) => window.URL.revokeObjectURL(f.url));
    if (clearFilesRef.current) {
      clearFilesRef.current();
    }
    setState("idle");
    setFormState({
      file: null,
      encryptionMethod: null,
      encryptionKey: null,
      aesSize: "128",
      rc5W: "32",
      rc5R: 12,
      rc5B: 16,
    });
    setDownloadFiles([]);
    setTimeTaken(null);
  }, [downloadFiles]);

  const handleDownload = (dlFile: DownloadFile) => {
    const link = document.createElement("a");
    link.href = dlFile.url;
    link.setAttribute("download", dlFile.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleGenerateRandomKey = async () => {
    if (!formState.encryptionMethod) return;

    setIsGeneratingKey(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      let endpoint = `${apiUrl}/${formState.encryptionMethod}/key`;
      if (formState.encryptionMethod === "aes") {
        endpoint = `${apiUrl}/aes/key?bits=${formState.aesSize}`;
      } else if (formState.encryptionMethod === "rc5") {
        endpoint = `${apiUrl}/rc5/key?b=${formState.rc5B}`;
      }

      const response = await axios.get(endpoint);

      if (response.data) {
        const key =
          formState.encryptionMethod === "hill"
            ? JSON.stringify(response.data.matrix)
            : (response.data.key?.toString() ?? "");
        setFormState((prev) => ({
          ...prev,
          encryptionKey: key,
        }));
      }
    } catch (error) {
      console.error("Key generation error:", error);
    } finally {
      setIsGeneratingKey(false);
    }
  };

  const handleEncrypt = async () => {
    playSound();

    const formData = new FormData();

    if (formState.file) {
      formData.append("file", formState.file);
    }
    if (formState.encryptionKey) {
      const key =
        formState.encryptionMethod === "hill"
          ? JSON.stringify({
              size: 2,
              matrix: JSON.parse(formState.encryptionKey),
            })
          : formState.encryptionKey;
      formData.append("key", key);
    }

    if (formState.encryptionMethod === "rc5") {
      formData.append("w", formState.rc5W);
      formData.append("r", formState.rc5R.toString());
    }

    setState("processing");
    const startTime = performance.now();

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.post(
        `${apiUrl}/${formState.encryptionMethod}/encrypt`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response);

      const files: DownloadFile[] = [];
      const baseName = formState.file?.name.replace(/\.[^.]+$/, "") || "file";
      const suffix = formState.encryptionMethod
        ? algoSuffixMap[formState.encryptionMethod] || ""
        : "";

      const encText = response.data.ciphertext || "";
      const encTextBlob = new Blob([encText], { type: "text/plain" });
      files.push({
        url: window.URL.createObjectURL(encTextBlob),
        filename: `${baseName}_Encrypted${suffix}.txt`,
        size: encTextBlob.size,
        label: "Encrypted",
      });

      if (response.data.key !== undefined && response.data.key !== null) {
        let keyStr = "";

        if (formState.encryptionMethod === "rc5") {
          keyStr =
            `Key: ${response.data.key}\nWord Size (w): ${formState.rc5W}-bit\n` +
            `Rounds (r): ${formState.rc5R}\nKey Size (b): ${formState.rc5B} bytes\n`;
        } else if (formState.encryptionMethod === "aes") {
          keyStr = `Key: ${response.data.key}\nKey Size: ${formState.aesSize}-bit\n`;
        } else {
          keyStr =
            typeof response.data.key === "object" && response.data.key.matrix
              ? JSON.stringify(response.data.key.matrix)
              : typeof response.data.key === "object"
                ? JSON.stringify(response.data.key)
                : String(response.data.key);
        }

        const keyBlob = new Blob([keyStr], { type: "text/plain" });
        files.push({
          url: window.URL.createObjectURL(keyBlob),
          filename: `${baseName}_Key${suffix}.txt`,
          size: keyBlob.size,
          label: "Key",
        });
      }

      setDownloadFiles(files);

      const endTime = performance.now();
      setTimeTaken((endTime - startTime) / 1000);

      setState("done");
    } catch (error) {
      console.error("Encryption error:", error);
      setState("error");
    }
  };

  return (
    <>
      <Header backButton titleText="Encrypt" />
      <main className="flex flex-col justify-center items-center gap-6 md:gap-10 p-4 md:p-6 w-full">
        <div className="flex flex-col justify-between items-center gap-6 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
          <div className="flex flex-col md:flex-row justify-between items-start gap-6 md:gap-10 w-full">
            <FileSelector
              titleText="Add Plaintext File"
              setFile={handleFileChange}
              state={state}
              className="w-full"
              onClearFilesReady={handleSetClear}
            />
            <div className="flex flex-col justify-center items-center gap-6 w-full">
              <Field>
                <FieldLabel htmlFor="input-button-group">
                  Encryption Method
                </FieldLabel>
                <Select
                  value={formState.encryptionMethod || ""}
                  onValueChange={(value) =>
                    setFormState((prev) => ({
                      ...prev,
                      encryptionMethod: value,
                      encryptionKey: null,
                      aesSize: "128",
                      rc5W: "32",
                      rc5R: 12,
                      rc5B: 16,
                    }))
                  }
                  disabled={state !== "idle"}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select encryption method" />
                  </SelectTrigger>
                  <SelectContent position="popper">
                    <SelectGroup>
                      <SelectItem value="caesar">Caesar Cipher</SelectItem>
                      <SelectItem value="permute">
                        Permutation Cipher
                      </SelectItem>
                      <SelectItem value="vigenere">Vigenère Cipher</SelectItem>
                      <SelectItem value="playfair">
                        Playfair Cipher (8x8)
                      </SelectItem>
                      <SelectItem value="hill">Hill Cipher (2x2)</SelectItem>
                      <SelectItem value="des">DES</SelectItem>
                      <SelectItem value="aes">AES</SelectItem>
                      <SelectItem value="rc5">RC5</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </Field>

              {formState.encryptionMethod === "aes" && (
                <Field>
                  <FieldLabel htmlFor="aes-size">AES Key Size</FieldLabel>
                  <Select
                    value={formState.aesSize}
                    onValueChange={(value) =>
                      setFormState((prev) => ({ ...prev, aesSize: value }))
                    }
                    disabled={state !== "idle"}
                  >
                    <SelectTrigger className="w-full" id="aes-size">
                      <SelectValue placeholder="Select size" />
                    </SelectTrigger>
                    <SelectContent position="popper">
                      <SelectGroup>
                        <SelectItem value="128">128-bit</SelectItem>
                        <SelectItem value="192">192-bit</SelectItem>
                        <SelectItem value="256">256-bit</SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </Field>
              )}

              {formState.encryptionMethod === "rc5" && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
                  <Field>
                    <FieldLabel htmlFor="rc5-w">Word Size (w)</FieldLabel>
                    <Select
                      value={formState.rc5W}
                      onValueChange={(value) =>
                        setFormState((prev) => ({ ...prev, rc5W: value }))
                      }
                      disabled={state !== "idle"}
                    >
                      <SelectTrigger className="w-full" id="rc5-w">
                        <SelectValue placeholder="Select w" />
                      </SelectTrigger>
                      <SelectContent position="popper">
                        <SelectGroup>
                          <SelectItem value="16">16-bit</SelectItem>
                          <SelectItem value="32">32-bit</SelectItem>
                          <SelectItem value="64">64-bit</SelectItem>
                        </SelectGroup>
                      </SelectContent>
                    </Select>
                  </Field>
                  <Field>
                    <FieldLabel htmlFor="rc5-r">Rounds (r)</FieldLabel>
                    <Input
                      id="rc5-r"
                      type="number"
                      min={0}
                      max={255}
                      value={formState.rc5R}
                      onChange={(e) => {
                        let val = parseInt(e.target.value);
                        if (isNaN(val)) val = 0;
                        val = Math.max(0, Math.min(255, val));
                        setFormState((prev) => ({
                          ...prev,
                          rc5R: val,
                        }));
                      }}
                      disabled={state !== "idle"}
                    />
                  </Field>
                  <Field>
                    <FieldLabel htmlFor="rc5-b">Key Size (b bytes)</FieldLabel>
                    <Input
                      id="rc5-b"
                      type="number"
                      min={0}
                      max={255}
                      value={formState.rc5B}
                      onChange={(e) => {
                        let val = parseInt(e.target.value);
                        if (isNaN(val)) val = 0;
                        val = Math.max(0, Math.min(255, val));
                        setFormState((prev) => ({
                          ...prev,
                          rc5B: val,
                        }));
                      }}
                      disabled={state !== "idle"}
                    />
                  </Field>
                </div>
              )}

              <Field>
                <FieldLabel htmlFor="input-button-group">
                  Encryption Key
                </FieldLabel>
                <ButtonGroup>
                  <Input
                    id="input-button-group"
                    placeholder="Enter Key"
                    value={formState.encryptionKey || ""}
                    onChange={(e) =>
                      setFormState((prev) => ({
                        ...prev,
                        encryptionKey: e.target.value,
                      }))
                    }
                    disabled={state !== "idle"}
                  />
                  <Button
                    variant="outline"
                    className="leading-none"
                    disabled={
                      state !== "idle" ||
                      !formState.encryptionMethod ||
                      isGeneratingKey
                    }
                    onClick={handleGenerateRandomKey}
                  >
                    {isGeneratingKey ? (
                      <IconLoader
                        className="size-4 animate-spin"
                        aria-hidden="true"
                      />
                    ) : (
                      <IconDice5 className="size-4" aria-hidden="true" />
                    )}
                    Random
                  </Button>
                </ButtonGroup>
              </Field>
            </div>
          </div>

          <div className="grid grid-cols-5 gap-2 w-full mt-2">
            <Button
              className="col-span-3 w-full leading-none"
              disabled={
                state !== "idle" ||
                !formState.file ||
                !formState.encryptionMethod ||
                !formState.encryptionKey
              }
              onClick={handleEncrypt}
            >
              {state === "processing" ? (
                <>
                  <IconLoader
                    className="size-4 animate-spin"
                    aria-hidden="true"
                  />
                  Encrypting...
                </>
              ) : state === "done" ? (
                <>
                  <IconCheck className="size-4" aria-hidden="true" />
                  Encrypted
                </>
              ) : state === "error" ? (
                <>
                  <IconX className="size-4" aria-hidden="true" />
                  Failed
                </>
              ) : (
                <>
                  <IconLock className="size-4" aria-hidden="true" /> Encrypt
                </>
              )}
            </Button>
            <Button
              className="col-span-2 w-full leading-none"
              variant="destructive"
              disabled={
                state === "processing" ||
                state === "done" ||
                (formState.file === null &&
                  !formState.encryptionMethod &&
                  !formState.encryptionKey)
              }
              onClick={handleClear}
            >
              <IconReload className="size-4" aria-hidden="true" />
              Reset
            </Button>
          </div>
        </div>

        {state === "done" && downloadFiles.length > 0 && (
          <div className="flex flex-col md:flex-row justify-between items-center gap-10 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <div className="flex flex-col justify-center items-start gap-5 text-sm text-muted-foreground w-full">
              <div className="flex flex-row flex-wrap justify-start items-center gap-1">
                <span className="flex justify-center items-center gap-1 leading-none">
                  <IconKey className="size-4 inline-block" aria-hidden="true" />
                  Encryption Key:
                </span>
                <span className="flex justify-center items-center gap-1.5 leading-none">
                  {formState.encryptionKey}
                  <Button
                    size="icon-lg"
                    variant="ghost"
                    className="size-4"
                    onClick={() => {
                      navigator.clipboard.writeText(
                        formState.encryptionKey || ""
                      );
                      setKeyCopied(true);
                      setTimeout(() => setKeyCopied(false), 2000);
                    }}
                    aria-label="Copy key to clipboard"
                  >
                    {keyCopied ? (
                      <IconCheck className="size-4" aria-hidden="true" />
                    ) : (
                      <IconCopy className="size-4" aria-hidden="true" />
                    )}
                  </Button>
                </span>
              </div>

              {timeTaken !== null && (
                <div className="flex items-center gap-1 leading-none">
                  <IconClock
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  Time Taken: {timeTaken.toFixed(2)} seconds
                </div>
              )}

              {downloadFiles.map((dlFile) => (
                <div
                  key={dlFile.filename}
                  className="flex items-center gap-1 leading-none"
                >
                  <IconFileInfo
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  {dlFile.label} File Size: {formatBytes(dlFile.size)}
                </div>
              ))}
            </div>
            <div className="flex flex-col justify-center items-center gap-4 w-full">
              {downloadFiles.map((dlFile) => (
                <Button
                  key={dlFile.filename}
                  title={dlFile.filename}
                  className="w-full leading-none"
                  variant="outline"
                  onClick={() => handleDownload(dlFile)}
                >
                  <IconDownload
                    className="size-4 shrink-0"
                    aria-hidden="true"
                  />
                  <span className="truncate">{dlFile.filename}</span>
                </Button>
              ))}

              <Button
                className="text-red-500 hover:text-red-400 w-full leading-none"
                variant="outline"
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Encrypt Another File
              </Button>
            </div>
          </div>
        )}

        {state === "error" && (
          <div className="flex flex-col justify-between items-center gap-4 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <p className="text-red-400 dark:text-red-800">
              An error occurred during encryption. Please check your inputs and
              try again.
            </p>

            <Button
              className="w-full"
              variant="outline"
              onClick={() => setState("idle")}
            >
              Try Again
            </Button>
          </div>
        )}
      </main>
    </>
  );
}
