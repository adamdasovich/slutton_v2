import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export default function GlassCard({ children, className = '', hover = true }: GlassCardProps) {
  return (
    <div className={`glass-card ${hover ? '' : 'hover:transform-none'} ${className}`}>
      {children}
    </div>
  );
}
