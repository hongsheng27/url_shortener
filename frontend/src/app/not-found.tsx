"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function NotFound() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full text-center px-6">
        <div className="mb-8">
          <h1 className="text-6xl font-bold text-gray-400 mb-4">404</h1>
        </div>
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Something&apos;s wrong here.
          </h2>

          <p className="text-gray-600 leading-relaxed">
            This is a 404 error, which means you&apos;ve clicked on a bad link
            or entered an invalid URL. Maybe what you are looking for can be
            found at{" "}
            <a
              href="https://bitly.com"
              className="text-blue-600 hover:text-blue-800 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              hungshengliu.xyz
            </a>
            .
          </p>
        </div>

        <div className="mt-8 space-y-4">
          <Link
            href="/"
            className="block w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Home
          </Link>
        </div>
      </div>
    </div>
  );
}
