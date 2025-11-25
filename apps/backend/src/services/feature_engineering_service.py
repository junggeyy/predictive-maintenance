import pandas as pd
import numpy as np

class FeatureEngineeringService:
   
    def extract_features(self, df):
      
        df = df.copy()
        
        # Ensure datetime is parsed
        if 'datetime' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['datetime']):
            df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Sort by machineID and datetime (required for rolling/lag features)
        df = df.sort_values(['machineID', 'datetime']).reset_index(drop=True)
        
        print("Creating features...")
        
        # 1. Rolling Window Features (16 features)
        df = self._create_rolling_features(df)
        
        # 2. Lag Features (12 features)
        df = self._create_lag_features(df)
        
        # 3. Event History Features (7 features)
        df = self._create_event_features(df)
        
        # 4. Machine-specific Features (8 features)
        df = self._create_machine_features(df)
        
        print(f"✓ Feature engineering complete! Added 43 features.")
        
        return df
    
    def _create_rolling_features(self, df):
        """Creates 16 rolling window features (6h & 24h mean/std for 4 sensors)"""
        sensors = ['volt', 'rotate', 'pressure', 'vibration']
        windows = [6, 24]
        stats = ['mean', 'std']
        
        for sensor in sensors:
            for window in windows:
                roll = df.groupby('machineID')[sensor].rolling(
                    window=window,
                    min_periods=1
                )
                
                for stat in stats:
                    feature_name = f'{sensor}_rolling_{window}h_{stat}'
                    
                    if stat == 'mean':
                        df[feature_name] = roll.mean().reset_index(0, drop=True)
                    elif stat == 'std':
                        df[feature_name] = roll.std().reset_index(0, drop=True)
        
        # Handle NaN values in std columns
        std_columns = [col for col in df.columns if '_std' in col and 'rolling' in col]
        df[std_columns] = df[std_columns].fillna(0)
        
        print("  Rolling features (16)")
        return df
    
    def _create_lag_features(self, df):
        """Creates 12 lag features (1h, 3h lags + 1h change for 4 sensors)"""
        sensors = ['volt', 'rotate', 'pressure', 'vibration']
        lag_hours = [1, 3]
        
        for sensor in sensors:
            # Lag values
            for lag in lag_hours:
                feature_name = f'{sensor}_lag_{lag}h'
                df[feature_name] = df.groupby('machineID')[sensor].shift(lag)
            
            # Rate of change
            feature_name = f'{sensor}_change_1h'
            df[feature_name] = df[sensor] - df.groupby('machineID')[sensor].shift(1)
        
        # Handle NaN values at start of each machine's time series
        lag_columns = [col for col in df.columns if '_lag_' in col or '_change_' in col]
        df[lag_columns] = df[lag_columns].fillna(0)
        
        print("   Lag features (12)")
        return df
    
    def _create_event_features(self, df):
        """Creates 7 event history features"""
        
        # Error count in last 24 hours
        df['error_count_last_24_h'] = df.groupby('machineID')['has_error'].rolling(
            window=24,
            min_periods=1
        ).sum().reset_index(0, drop=True)
        
        # Hours since last error
        df['hours_since_last_error'] = np.nan
        for machine_id in df['machineID'].unique():
            mask = df['machineID'] == machine_id
            machine_df = df[mask].copy()
            error_indices = machine_df[machine_df['has_error'] == 1].index
            
            for i in machine_df.index:
                prev_errors = error_indices[error_indices < i]
                if len(prev_errors) > 0:
                    last_error_index = prev_errors[-1]
                    last_error_time = machine_df.loc[last_error_index, 'datetime']
                    current_time = machine_df.loc[i, 'datetime']
                    dif_hours = (current_time - last_error_time).total_seconds() / 3600
                    df.loc[i, 'hours_since_last_error'] = dif_hours
                else:
                    df.loc[i, 'hours_since_last_error'] = 999
        
        # Hours since last maintenance
        df['hours_since_last_maintenance'] = np.nan
        for machine_id in df['machineID'].unique():
            mask = df['machineID'] == machine_id
            machine_df = df[mask].copy()
            maint_indices = machine_df[machine_df['has_maintenance'] == 1].index
            
            for i in machine_df.index:
                prev_maint = maint_indices[maint_indices < i]
                if len(prev_maint) > 0:
                    last_maint_index = prev_maint[-1]
                    last_maint_time = machine_df.loc[last_maint_index, 'datetime']
                    current_time = machine_df.loc[i, 'datetime']
                    dif_hours = (current_time - last_maint_time).total_seconds() / 3600
                    df.loc[i, 'hours_since_last_maintenance'] = dif_hours
                else:
                    df.loc[i, 'hours_since_last_maintenance'] = 999
        
        # Days since last failure
        df['days_since_last_failure'] = np.nan
        for machine_id in df['machineID'].unique():
            mask = df['machineID'] == machine_id
            machine_df = df[mask].copy()
            failure_indices = machine_df[machine_df['has_failure'] == 1].index
            
            for i in machine_df.index:
                prev_failures = failure_indices[failure_indices < i]
                if len(prev_failures) > 0:
                    last_failure_index = prev_failures[-1]
                    last_failure_time = machine_df.loc[last_failure_index, 'datetime']
                    current_time = machine_df.loc[i, 'datetime']
                    dif_days = (current_time - last_failure_time).total_seconds() / (3600 * 24)
                    df.loc[i, 'days_since_last_failure'] = dif_days
                else:
                    df.loc[i, 'days_since_last_failure'] = 999
        
        # Cumulative event counts
        df['total_errors_to_date'] = df.groupby('machineID')['has_error'].cumsum()
        df['total_maintenances_to_date'] = df.groupby('machineID')['has_maintenance'].cumsum()
        df['total_failures_to_date'] = df.groupby('machineID')['has_failure'].cumsum()
        
        print("  ✓ Event features (7)")
        return df
    
    def _create_machine_features(self, df):
        """Creates 8 machine-specific features"""
        
        # One-hot encode machine models
        dummies_model = pd.get_dummies(df['model'], drop_first=True)
        df = pd.concat([df, dummies_model], axis=1)
        
        # Age squared
        df['age_squared'] = df['age'] ** 2
        
        # Machine baseline deviations
        sensors = ['volt', 'rotate', 'pressure', 'vibration']
        for sensor in sensors:
            machine_avg = df.groupby('machineID')[sensor].transform('mean')
            feature_name = f'{sensor}_deviation_from_machine_avg'
            df[feature_name] = df[sensor] - machine_avg
        
        print("   Machine features (8)")
        return df

feature_engineering_service = FeatureEngineeringService()