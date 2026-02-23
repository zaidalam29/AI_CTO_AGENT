// src/app/providers.tsx
'use client';

import { ReactNode } from 'react';

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  return (
    <>
      {/* Add any providers here (Theme, Auth, etc.) */}
      {children}
    </>
  );
}