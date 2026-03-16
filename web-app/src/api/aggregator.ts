/**
 * API client for bank data aggregation (Plaid + Akoya).
 *
 * Uses direct axios calls since the SDK hasn't been regenerated
 * with the new /api/link/* endpoints yet.
 */

import axios from 'axios';
import type {
  LinkedProvider,
  SyncResult,
  LinkTokenResponse,
  AkoyaAuthUrlResponse,
} from '../types/aggregator';

const baseUrl =
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8080');

const api = axios.create({ baseURL: `${baseUrl}/api/link` });

// --- Plaid ---

export const createPlaidLinkToken = async (): Promise<LinkTokenResponse> => {
  const response = await api.post('/plaid/token');
  return response.data;
};

export const exchangePlaidToken = async (
  publicToken: string,
  institutionId?: string,
  institutionName?: string,
): Promise<LinkedProvider> => {
  const response = await api.post('/plaid/exchange', {
    public_token: publicToken,
    institution_id: institutionId,
    institution_name: institutionName,
  });
  return response.data;
};

// --- Akoya ---

export const getAkoyaAuthUrl = async (
  providerId: string = 'fidelity',
): Promise<AkoyaAuthUrlResponse> => {
  const response = await api.get('/akoya/authorize', {
    params: { provider_id: providerId },
  });
  return response.data;
};

export const exchangeAkoyaCode = async (
  authCode: string,
  providerId: string = 'fidelity',
): Promise<LinkedProvider> => {
  const response = await api.post('/akoya/callback', {
    auth_code: authCode,
    provider_id: providerId,
  });
  return response.data;
};

// --- Provider management ---

export const getLinkedProviders = async (): Promise<LinkedProvider[]> => {
  const response = await api.get('/providers');
  return response.data;
};

export const getLinkedProvider = async (id: number): Promise<LinkedProvider> => {
  const response = await api.get(`/providers/${id}`);
  return response.data;
};

export const syncProvider = async (id: number): Promise<SyncResult> => {
  const response = await api.post(`/providers/${id}/sync`);
  return response.data;
};

export const unlinkProvider = async (id: number): Promise<void> => {
  await api.delete(`/providers/${id}`);
};
