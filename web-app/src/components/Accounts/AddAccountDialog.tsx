import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  InputAdornment,
  Alert,
  Divider,
  Typography,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import { createAccount, getAccounts } from '../../api/accounts';
import {
  AccountCreate,
  AccountType,
  PropertyType,
  getAccountTypeLabel,
} from '../../types/account';
import { useEntityContext } from '../../contexts/EntityContext';
import { ENTITY_TYPE_LABELS } from '../../types/entity';

interface AddAccountDialogProps {
  open: boolean;
  onClose: () => void;
  onAccountCreated: () => void;
}

const AddAccountDialog: React.FC<AddAccountDialogProps> = ({
  open,
  onClose,
  onAccountCreated,
}) => {
  const [formData, setFormData] = useState<AccountCreate>({
    account_name: '',
    account_type: 'checking',
    institution_name: '',
    account_number_last4: '',
    opening_balance: 0,
    opening_balance_date: new Date().toISOString().split('T')[0],
    notes: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const { enqueueSnackbar } = useSnackbar();
  const { entities, selectedEntityId } = useEntityContext();
  const [entityIds, setEntityIds] = useState<number[]>(
    selectedEntityId != null ? [selectedEntityId] : []
  );

  const { data: loanAccounts = [] } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => getAccounts(),
    select: (data) => data.filter((a) => a.account_type === 'loan'),
  });

  const createMutation = useMutation({
    mutationFn: createAccount,
    onSuccess: () => {
      enqueueSnackbar('Account created', { variant: 'success' });
      onAccountCreated();
      handleClose();
    },
    onError: () => {
      enqueueSnackbar('Failed to create account', { variant: 'error' });
    },
  });

  const handleClose = () => {
    setFormData({
      account_name: '',
      account_type: 'checking',
      institution_name: '',
      account_number_last4: '',
      opening_balance: 0,
      opening_balance_date: new Date().toISOString().split('T')[0],
      notes: '',
    });
    setEntityIds(selectedEntityId != null ? [selectedEntityId] : []);
    setErrors({});
    onClose();
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.account_name.trim()) {
      newErrors.account_name = 'Account name is required';
    }

    if (formData.account_number_last4 && !/^\d{4}$/.test(formData.account_number_last4)) {
      newErrors.account_number_last4 = 'Must be exactly 4 digits';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      const dataWithEntity = {
        ...formData,
        entity_ids: entityIds.length > 0 ? entityIds : undefined,
      };
      createMutation.mutate(dataWithEntity);
    }
  };

  const handleInputChange = (
    field: keyof AccountCreate,
    value: string | number | null | undefined
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));

    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const accountTypes: AccountType[] = [
    'checking',
    'savings',
    'brokerage',
    'investment',
    'credit_card',
    'loan',
    '401k',
    'ira',
    'real_estate',
    'other',
  ];

  const isRealEstate = formData.account_type === 'real_estate';

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add New Account</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          {createMutation.isError && (
            <Grid item xs={12}>
              <Alert severity="error">
                Error creating account. Please try again.
              </Alert>
            </Grid>
          )}

          <Grid item xs={12}>
            <TextField
              label="Account Name"
              fullWidth
              required
              value={formData.account_name}
              onChange={(e) => handleInputChange('account_name', e.target.value)}
              error={!!errors.account_name}
              helperText={errors.account_name}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth required>
              <InputLabel>Account Type</InputLabel>
              <Select
                value={formData.account_type}
                onChange={(e) =>
                  handleInputChange('account_type', e.target.value as AccountType)
                }
                label="Account Type"
              >
                {accountTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {getAccountTypeLabel(type)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              label="Institution"
              fullWidth
              value={formData.institution_name || ''}
              onChange={(e) => handleInputChange('institution_name', e.target.value)}
              placeholder="e.g., Chase Bank"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Currency</InputLabel>
              <Select
                value={formData.currency || 'USD'}
                onChange={(e) => handleInputChange('currency', e.target.value)}
                label="Currency"
              >
                {['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'CNY', 'INR', 'BRL', 'MXN', 'KRW', 'SEK', 'NOK', 'DKK', 'NZD', 'SGD', 'HKD', 'TWD', 'ZAR'].map((code) => (
                  <MenuItem key={code} value={code}>{code}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              label="Last 4 Digits"
              fullWidth
              value={formData.account_number_last4 || ''}
              onChange={(e) => {
                const val = e.target.value.replace(/\D/g, '').slice(0, 4);
                handleInputChange('account_number_last4', val);
              }}
              error={!!errors.account_number_last4}
              helperText={errors.account_number_last4 || 'Account number last 4 digits'}
              inputProps={{ maxLength: 4, pattern: '[0-9]*' }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              label="Opening Balance"
              fullWidth
              type="number"
              value={formData.opening_balance || 0}
              onChange={(e) =>
                handleInputChange('opening_balance', parseFloat(e.target.value) || 0)
              }
              InputProps={{
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
              }}
            />
          </Grid>

          <Grid item xs={12}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Opening Balance Date"
                value={
                  formData.opening_balance_date
                    ? new Date(formData.opening_balance_date)
                    : new Date()
                }
                onChange={(newDate) => {
                  if (newDate) {
                    handleInputChange(
                      'opening_balance_date',
                      newDate.toISOString().split('T')[0]
                    );
                  }
                }}
                slotProps={{
                  textField: {
                    fullWidth: true,
                  },
                }}
              />
            </LocalizationProvider>
          </Grid>

          {isRealEstate && (
            <>
              <Grid item xs={12}>
                <Divider>
                  <Typography variant="caption" color="text.secondary">Real Estate Details</Typography>
                </Divider>
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  label="Property Value"
                  fullWidth
                  type="number"
                  value={formData.property_value ?? ''}
                  onChange={(e) =>
                    handleInputChange('property_value', parseFloat(e.target.value) || 0)
                  }
                  InputProps={{
                    startAdornment: <InputAdornment position="start">$</InputAdornment>,
                  }}
                  helperText="Current market value of the property"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Property Type</InputLabel>
                  <Select
                    value={formData.property_type ?? ''}
                    onChange={(e) =>
                      handleInputChange('property_type', e.target.value as PropertyType)
                    }
                    label="Property Type"
                  >
                    <MenuItem value="primary_residence">Primary Residence</MenuItem>
                    <MenuItem value="rental">Rental Property</MenuItem>
                    <MenuItem value="vacation">Vacation Home</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {loanAccounts.length > 0 && (
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Linked Mortgage / Loan</InputLabel>
                    <Select
                      value={formData.linked_mortgage_account_id ?? ''}
                      onChange={(e) =>
                        handleInputChange(
                          'linked_mortgage_account_id',
                          e.target.value ? Number(e.target.value) : null
                        )
                      }
                      label="Linked Mortgage / Loan"
                    >
                      <MenuItem value="">None</MenuItem>
                      {loanAccounts.map((acc) => (
                        <MenuItem key={acc.account_id} value={acc.account_id}>
                          {acc.account_name}
                          {acc.institution_name ? ` — ${acc.institution_name}` : ''}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              )}
            </>
          )}

          <Grid item xs={12}>
            <TextField
              label="Notes"
              fullWidth
              multiline
              rows={3}
              value={formData.notes || ''}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              placeholder="Optional notes about this account"
            />
          </Grid>

          {entities.length > 0 && (
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Entities</InputLabel>
                <Select
                  multiple
                  value={entityIds}
                  label="Entities"
                  onChange={(e) => setEntityIds(e.target.value as number[])}
                  renderValue={(selected) =>
                    (selected as number[])
                      .map((id) => entities.find((ent) => ent.entity_id === id)?.entity_name)
                      .filter(Boolean)
                      .join(', ')
                  }
                >
                  {entities.map((entity) => (
                    <MenuItem key={entity.entity_id} value={entity.entity_id}>
                      {entity.entity_name} ({ENTITY_TYPE_LABELS[entity.entity_type] || entity.entity_type})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={createMutation.isPending}
        >
          {createMutation.isPending ? 'Creating...' : 'Create Account'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddAccountDialog;