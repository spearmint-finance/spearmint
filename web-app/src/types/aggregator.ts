export interface LinkedProvider {
  id: number;
  provider_type: 'plaid' | 'akoya';
  institution_id?: string;
  institution_name?: string;
  status: 'active' | 'login_required' | 'error' | 'revoked';
  error_code?: string;
  error_message?: string;
  last_synced_at?: string;
  created_at: string;
  account_count: number;
}

export interface SyncResult {
  transactions_added: number;
  transactions_modified: number;
  transactions_removed: number;
  balances_updated: number;
  holdings_updated: number;
}

export interface LinkTokenResponse {
  link_token: string;
  expiration: string;
}

export interface AkoyaAuthUrlResponse {
  authorization_url: string;
  provider_id: string;
}
