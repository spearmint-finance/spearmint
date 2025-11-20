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
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useMutation } from '@tanstack/react-query';
import { createAccount } from '../../api/accounts';
import {
  AccountCreate,
  AccountType,
  getAccountTypeLabel,
} from '../../types/account';

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

  const createMutation = useMutation({
    mutationFn: createAccount,
    onSuccess: () => {
      onAccountCreated();
      handleClose();
    },
    onError: (error: any) => {
      console.error('Error creating account:', error);
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
      createMutation.mutate(formData);
    }
  };

  const handleInputChange = (
    field: keyof AccountCreate,
    value: string | number | null
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
    'other',
  ];

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
            <TextField
              label="Last 4 Digits"
              fullWidth
              value={formData.account_number_last4 || ''}
              onChange={(e) => handleInputChange('account_number_last4', e.target.value)}
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