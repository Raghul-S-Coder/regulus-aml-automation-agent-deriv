import { useCallback, useEffect, useState } from "react";

type ApiState<T> = {
  data: T | null;
  error: string | null;
  loading: boolean;
};

export function useApi<T>(
  fetcher: () => Promise<T>,
  deps: unknown[] = [],
  refreshMs?: number
) {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    error: null,
    loading: true
  });
  const [refreshKey, setRefreshKey] = useState(0);

  const refetch = useCallback(() => {
    setRefreshKey((k) => k + 1);
  }, []);

  useEffect(() => {
    let isMounted = true;
    let intervalId: number | undefined;

    const run = () => {
      setState((prev) => ({
        ...prev,
        loading: prev.data === null,
        error: null
      }));
      fetcher()
        .then((data) => {
          if (isMounted) {
            setState({ data, error: null, loading: false });
          }
        })
        .catch((error: Error) => {
          if (isMounted) {
            setState({ data: null, error: error.message, loading: false });
          }
        });
    };

    run();
    if (refreshMs && refreshMs > 0) {
      intervalId = window.setInterval(run, refreshMs);
    }

    return () => {
      isMounted = false;
      if (intervalId) {
        window.clearInterval(intervalId);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, refreshKey]);

  return { ...state, refetch };
}
