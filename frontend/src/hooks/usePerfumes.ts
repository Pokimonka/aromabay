import { useState, useEffect } from 'react';
import type { Perfume } from '../types';
import { perfumeService } from '../services/perfumes';

export const usePerfumes = (filters?: {
  search?: string;
  sort?: string;
}) => {
  const [perfumes, setPerfumes] = useState<Perfume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPerfumes();
  }, [filters?.search, filters?.sort]);

  const loadPerfumes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await perfumeService.getPerfumes(filters);
      setPerfumes(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load perfumes');
    } finally {
      setLoading(false);
    }
  };

  const refetch = () => {
    loadPerfumes();
  };

  return {
    perfumes,
    loading,
    error,
    refetch,
  };
};