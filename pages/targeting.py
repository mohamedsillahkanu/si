# Data merging section
st.subheader("Merge Data")

if len(st.session_state.dataframes) >= 2:
    col1, col2 = st.columns(2)
    
    with col1:
        base_data = st.selectbox(
            "Select base dataset:",
            list(st.session_state.dataframes.keys()),
            key="base_data_selector"
        )
    
    with col2:
        merge_data = st.selectbox(
            "Select dataset to merge with base:",
            [f for f in list(st.session_state.dataframes.keys()) if f != base_data],
            key="merge_data_selector"
        )
    
    if base_data and merge_data:
        df1 = st.session_state.dataframes[base_data]
        df2 = st.session_state.dataframes[merge_data]
        
        # Find common columns
        common_columns = list(set(df1.columns) & set(df2.columns))
        
        if common_columns:
            st.write(f"Found {len(common_columns)} common columns: {', '.join(common_columns)}")
            
            # Use all common columns as join keys by default
            st.info("Using all common columns for merging with left join and validate='1:1'")
            
            if st.button("Merge Datasets"):
                try:
                    merged_df = df1.merge(
                        df2,
                        on=common_columns,  # Use all common columns automatically
                        how='left',         # Use left join by default
                        validate="1:1",     # Enforce 1:1 relationship
                        suffixes=('', f'_{merge_data}')
                    )
                    
                    st.session_state.merged_df = merged_df
                    st.session_state.join_keys = common_columns
                    st.success(f"Successfully merged datasets. Result has {len(merged_df)} rows and {len(merged_df.columns)} columns.")
                    
                    st.write("Preview of merged data:")
                    st.write(merged_df.head())
                except Exception as e:
                    st.error(f"Error merging datasets: {e}")
        else:
            st.warning("No common columns found between selected datasets.")
else:
    st.info("Upload at least two datasets to perform merging.")

# Similar update for merging with shapefile
if st.session_state.merged_df is not None and st.session_state.shapefile is not None:
    st.subheader("Merge with Shapefile")
    
    gdf = st.session_state.shapefile
    
    # Find common columns
    common_columns = list(set(st.session_state.merged_df.columns) & set(gdf.columns))
    
    if common_columns:
        st.write(f"Found {len(common_columns)} common columns between data and shapefile: {', '.join(common_columns)}")
        
        # Use all common columns by default
        st.info("Using all common columns for merging with shapefile using left join and validate='1:1'")
        
        if st.button("Merge with Shapefile"):
            try:
                # Clean string columns in shapefile if they're join keys
                for key in common_columns:
                    if gdf[key].dtype == 'object':
                        gdf[key] = gdf[key].astype(str).str.strip()
                
                # Merge
                merged_gdf = gdf.merge(
                    st.session_state.merged_df,
                    on=common_columns,  # Use all common columns
                    how='left',         # Use left join
                    validate="1:1"      # Enforce 1:1 relationship
                )
                
                st.session_state.merged_gdf = merged_gdf
                st.success(f"Successfully merged data with shapefile. Result has {len(merged_gdf)} features.")
                
                st.write("Preview of merged geodataframe:")
                st.write(merged_gdf.head())
            except Exception as e:
                st.error(f"Error merging with shapefile: {e}")
    else:
        st.warning("No common columns found between data and shapefile.")
