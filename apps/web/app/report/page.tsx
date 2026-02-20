"use client";

import axios from "axios";
import { useCallback, useRef, useState } from "react";
import Header from "@/components/Header";
import { Button } from "@workspace/ui/components/button";
import { formatBytes } from "@/hooks/use-file-upload";
import type { State } from "@/components/FileSelector";
import FileSelector from "@/components/FileSelector";
import {
  IconCheck,
  IconClock,
  IconDownload,
  IconFileInfo,
  IconLoader,
  IconReload,
  IconPercentage,
  IconAbc,
  IconLineHeight,
  IconAlphabetLatin,
  IconRuler2,
  IconPresentationAnalytics,
  IconDeviceAnalytics,
  IconX,
} from "@tabler/icons-react";

interface ReportStats {
  overallAccuracy: string;
  lengthDifference: string;
  originalLength: string;
  decryptedLength: string;
  alphabetAccuracy: string;
  nonAlphaAccuracy: string;
  wordAccuracy: string;
  lineAccuracy: string;
  verdict: string;
}

function parseReportStats(reportText: string): ReportStats {
  const lines = reportText.split("\n");
  const get = (prefix: string) =>
    lines
      .find((l) => l.startsWith(prefix))
      ?.replace(prefix, "")
      .trim() ?? "N/A";

  return {
    overallAccuracy: get("Overall accuracy:"),
    lengthDifference: get("Length difference:"),
    originalLength: get("Original File Length:"),
    decryptedLength: get("Decrypted File Length:"),
    alphabetAccuracy: get("Alphabet accuracy:"),
    nonAlphaAccuracy: get("Non-alpha accuracy:"),
    wordAccuracy: get("Word accuracy:"),
    lineAccuracy: get("Line accuracy:"),
    verdict: get("VERDICT:"),
  };
}

export default function Report() {
  const [state, setState] = useState<State>("idle");
  const [originalFile, setOriginalFile] = useState<File | null>(null);
  const [attackedFile, setAttackedFile] = useState<File | null>(null);
  const [reportFile, setReportFile] = useState<{
    url: string;
    filename: string;
    size: number;
  } | null>(null);
  const [reportStats, setReportStats] = useState<ReportStats | null>(null);
  const [timeTaken, setTimeTaken] = useState<number | null>(null);
  const clearOriginalRef = useRef<(() => void) | null>(null);
  const clearAttackedRef = useRef<(() => void) | null>(null);

  const handleOriginalFileChange = useCallback((file: File | null) => {
    setOriginalFile(file);
  }, []);

  const handleAttackedFileChange = useCallback((file: File | null) => {
    setAttackedFile(file);
  }, []);

  const handleSetClearOriginal = useCallback((clearFn: () => void) => {
    clearOriginalRef.current = clearFn;
  }, []);

  const handleSetClearAttacked = useCallback((clearFn: () => void) => {
    clearAttackedRef.current = clearFn;
  }, []);

  const handleClear = useCallback(() => {
    if (reportFile) {
      window.URL.revokeObjectURL(reportFile.url);
    }
    clearOriginalRef.current?.();
    clearAttackedRef.current?.();
    setState("idle");
    setOriginalFile(null);
    setAttackedFile(null);
    setReportFile(null);
    setReportStats(null);
    setTimeTaken(null);
  }, [reportFile]);

  const handleDownload = () => {
    if (!reportFile) return;

    const link = document.createElement("a");
    link.href = reportFile.url;
    link.setAttribute("download", reportFile.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleGenerateReport = async () => {
    if (!originalFile || !attackedFile) return;

    const formData = new FormData();
    formData.append("original", originalFile);
    formData.append("recovered", attackedFile);

    setState("processing");
    const startTime = performance.now();

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await axios.post(`${apiUrl}/report`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });

      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);

      const contentDisposition = response.headers["content-disposition"];
      let filename = `${originalFile.name.replace(/\.[^.]+$/, "")}_comparison_report.txt`;
      if (contentDisposition) {
        filename = contentDisposition
          .split(";")[1]
          .split("=")[1]
          .replace(/"/g, "");
      }

      const reportText = await blob.text();
      const stats = parseReportStats(reportText);
      setReportStats(stats);

      setReportFile({ url, filename, size: blob.size });

      const endTime = performance.now();
      setTimeTaken((endTime - startTime) / 1000);

      setState("done");
    } catch (error) {
      console.error("Report generation error:", error);
      setState("error");
    }
  };

  return (
    <>
      <Header backButton titleText="Generate Report" />
      <main className="flex flex-col justify-center items-center gap-6 md:gap-10 p-4 md:p-6 w-full">
        <div className="flex flex-col justify-between items-center gap-6 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
          <div className="flex flex-col md:flex-row justify-between items-start gap-6 md:gap-10 w-full">
            <FileSelector
              titleText="Add Original File"
              setFile={handleOriginalFileChange}
              state={state}
              className="w-full"
              onClearFilesReady={handleSetClearOriginal}
            />
            <FileSelector
              titleText="Add Recovered File"
              setFile={handleAttackedFileChange}
              state={state}
              className="w-full"
              onClearFilesReady={handleSetClearAttacked}
            />
          </div>

          <div className="grid grid-cols-5 gap-2 w-full mt-2">
            <Button
              className="col-span-3 w-full leading-none"
              disabled={state !== "idle" || !originalFile || !attackedFile}
              onClick={handleGenerateReport}
            >
              {state === "processing" ? (
                <>
                  <IconLoader
                    className="size-4 animate-spin"
                    aria-hidden="true"
                  />
                  Generating...
                </>
              ) : state === "done" ? (
                <>
                  <IconCheck className="size-4" aria-hidden="true" />
                  Generated
                </>
              ) : state === "error" ? (
                <>
                  <IconX className="size-4" aria-hidden="true" />
                  Failed
                </>
              ) : (
                <>
                  <IconDeviceAnalytics className="size-4" aria-hidden="true" />
                  Generate Report
                </>
              )}
            </Button>
            <Button
              className="col-span-2 w-full leading-none"
              variant="destructive"
              disabled={
                state === "processing" ||
                state === "done" ||
                (!originalFile && !attackedFile)
              }
              onClick={handleClear}
            >
              <IconReload className="size-4" aria-hidden="true" />
              Reset
            </Button>
          </div>
        </div>

        {state === "done" && reportStats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <div className="flex flex-col justify-center items-start gap-4 text-sm text-muted-foreground">
              {reportFile && (
                <div className="flex items-center gap-1 leading-none">
                  <IconFileInfo
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  File Size: <b>{formatBytes(reportFile.size)}</b>
                </div>
              )}
              {timeTaken !== null && (
                <div className="flex items-center gap-1 leading-none">
                  <IconClock
                    className="size-4 inline-block"
                    aria-hidden="true"
                  />
                  Time Taken: <b>{timeTaken.toFixed(2)}s</b>
                </div>
              )}
              <div className="flex items-center gap-1 leading-none">
                <IconPresentationAnalytics
                  className="size-4 inline-block"
                  aria-hidden="true"
                />
                Verdict: <b>{reportStats.verdict}</b>
              </div>
              <div className="flex items-center gap-1 leading-none">
                <IconRuler2
                  className="size-4 inline-block"
                  aria-hidden="true"
                />
                Length Difference: <b>{reportStats.lengthDifference}</b>
              </div>
            </div>

            <div className="flex flex-col justify-center items-start gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-1 leading-none">
                <IconPercentage
                  className="size-4 inline-block"
                  aria-hidden="true"
                />
                Overall Accuracy: <b>{reportStats.overallAccuracy}</b>
              </div>
              <div className="flex items-center gap-1 leading-none">
                <IconLineHeight
                  className="size-4 inline-block"
                  aria-hidden="true"
                />
                Line Accuracy: <b>{reportStats.lineAccuracy}</b>
              </div>
              <div className="flex items-center gap-1 leading-none">
                <IconAbc className="size-4 inline-block" aria-hidden="true" />
                Word Accuracy: <b>{reportStats.wordAccuracy}</b>
              </div>
              <div className="flex items-center gap-1 leading-none">
                <IconAlphabetLatin
                  className="size-4 inline-block"
                  aria-hidden="true"
                />
                Alphabet Accuracy: <b>{reportStats.alphabetAccuracy}</b>
              </div>
            </div>

            <div className="flex flex-col justify-center items-center gap-6 md:gap-8">
              <Button
                className="w-full leading-none"
                variant="outline"
                onClick={handleDownload}
              >
                <IconDownload className="size-4" aria-hidden="true" />
                {reportFile?.filename || "N/A"}
              </Button>

              <Button
                className="text-red-500 hover:text-red-400 w-full leading-none"
                variant="outline"
                onClick={handleClear}
              >
                <IconReload className="size-4" aria-hidden="true" />
                Another Report
              </Button>
            </div>
          </div>
        )}

        {state === "error" && (
          <div className="flex flex-col justify-between items-center gap-4 p-4 md:p-6 w-full max-w-6xl border rounded-lg">
            <p className="text-red-400 dark:text-red-800">
              An error occurred while generating the report. Please check your
              files and try again.
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
