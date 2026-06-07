import { useState, useEffect, useCallback, useRef } from "react";

/**
 * useApi — generic hook for API calls with loading / error / data states.
 *
 * Usage:
 *   const { data, loading, error, refetch } = useApi(productsApi.getAll, { search: "shirt" });
 *
 * @param {Function} apiFn  — the API function to call (must return a Promise)
 * @param {any}      params — params passed to apiFn; changing this re-fetches
 * @param {object}   opts   — { immediate: bool (default true), deps: [] }
 */
export function useApi(apiFn, params = undefined, opts = {}) {
  const { immediate = true } = opts;
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState(null);
  const abortRef = useRef(null);

  const fetch = useCallback(
    async (overrideParams) => {
      setLoading(true);
      setError(null);
      try {
        const result = await apiFn(overrideParams ?? params);
        setData(result);
        return result;
      } catch (err) {
        setError(err.message || "Error fetching data");
        return null;
      } finally {
        setLoading(false);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [apiFn, JSON.stringify(params)]
  );

  useEffect(() => {
    if (immediate) {
      fetch();
    }
    return () => {
      // cleanup: nothing to abort in axios without cancel tokens
    };
  }, [fetch, immediate]);

  return { data, loading, error, refetch: fetch };
}

/**
 * useMutation — hook for write operations (create, update, delete).
 *
 * Usage:
 *   const { mutate, loading, error } = useMutation(productsApi.create);
 *   await mutate(payload);
 */
export function useMutation(apiFn) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mutate = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        const result = await apiFn(...args);
        return { data: result, error: null };
      } catch (err) {
        const msg = err.message || "Operation failed";
        setError(msg);
        return { data: null, error: msg };
      } finally {
        setLoading(false);
      }
    },
    [apiFn]
  );

  return { mutate, loading, error };
}
