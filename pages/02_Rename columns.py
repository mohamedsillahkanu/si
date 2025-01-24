rename_columns <- function(df) {
 tryCatch({
   # Define mapping dictionaries
   orgunit_rename <- c(
     orgunitlevel1 = "adm0",
     orgunitlevel2 = "adm1",
     orgunitlevel3 = "adm2",
     orgunitlevel4 = "adm3",
     organisationunitname = "hf"
   )

   column_rename <- c(
     "OPD (New and follow-up curative) 0-59m_X" = "allout_u5",
     "OPD (New and follow-up curative) 5+y_X" = "allout_ov5",

     "Admission - Child with malaria 0-59 months_X" = "maladm_u5",
     "Admission - Child with malaria 5-14 years_X" = "maladm_5_14",
     "Admission - Malaria 15+ years_X" = "maladm_ov15",

     "Child death - Malaria 1-59m_X" = "maldth_1_59m",
     "Child death - Malaria 10-14y_X" = "maldth_10_14",
     "Child death - Malaria 5-9y_X" = "maldth_5_9",

     "Death malaria 15+ years Female" = "maldth_fem_ov15",
     "Death malaria 15+ years Male" = "maldth_mal_ov15",

     "Separation - Child with malaria 0-59 months_X Death" = "maldth_u5",
     "Separation - Child with malaria 5-14 years_X Death" = "maldth_5_14",
     "Separation - Malaria 15+ years_X Death" = "maldth_ov15",

     "Fever case - suspected Malaria 0-59m_X" = "susp_u5_hf",
     "Fever case - suspected Malaria 5-14y_X" = "susp_5_14_hf",
     "Fever case - suspected Malaria 15+y_X" = "susp_ov15_hf",
     "Fever case in community (Suspected Malaria) 0-59m_X" = "susp_u5_com",
     "Fever case in community (Suspected Malaria) 5-14y_X" = "susp_5_14_com",
     "Fever case in community (Suspected Malaria) 15+y_X" = "susp_ov15_com",

     "Fever case in community tested for Malaria (RDT) - Negative 0-59m_X" = "tes_neg_rdt_u5_com",
     "Fever case in community tested for Malaria (RDT) - Positive 0-59m_X" = "tes_pos_rdt_u5_com",
     "Fever case in community tested for Malaria (RDT) - Negative 5-14y_X" = "tes_neg_rdt_5_14_com",
     "Fever case in community tested for Malaria (RDT) - Positive 5-14y_X" = "tes_pos_rdt_5_14_com",
     "Fever case in community tested for Malaria (RDT) - Negative 15+y_X" = "tes_neg_rdt_ov15_com",
     "Fever case in community tested for Malaria (RDT) - Positive 15+y_X" = "tes_pos_rdt_ov15_com",
     "Fever case tested for Malaria (Microscopy) - Negative 0-59m_X" = "test_neg_mic_u5_hf",
     "Fever case tested for Malaria (Microscopy) - Positive 0-59m_X" = "test_pos_mic_u5_hf",
     "Fever case tested for Malaria (Microscopy) - Negative 5-14y_X" = "test_neg_mic_5_14_hf",
     "Fever case tested for Malaria (Microscopy) - Positive 5-14y_X" = "test_pos_mic_5_14_hf",
     "Fever case tested for Malaria (Microscopy) - Negative 15+y_X" = "test_neg_mic_ov15_hf",
     "Fever case tested for Malaria (Microscopy) - Positive 15+y_X" = "test_pos_mic_ov15_hf",
     "Fever case tested for Malaria (RDT) - Negative 0-59m_X" = "tes_neg_rdt_u5_hf",
     "Fever case tested for Malaria (RDT) - Positive 0-59m_X" = "tes_pos_rdt_u5_hf",
     "Fever case tested for Malaria (RDT) - Negative 5-14y_X" = "tes_neg_rdt_5_14_hf",
     "Fever case tested for Malaria (RDT) - Positive 5-14y_X" = "tes_pos_rdt_5_14_hf",
     "Fever case tested for Malaria (RDT) - Negative 15+y_X" = "tes_neg_rdt_ov15_hf",
     "Fever case tested for Malaria (RDT) - Positive 15+y_X" = "tes_pos_rdt_ov15_hf",

     "Malaria treated in community with ACT <24 hours 0-59m_X" = "maltreat_u24_u5_com",
     "Malaria treated in community with ACT >24 hours 0-59m_X" = "maltreat_ov24_u5_com",
     "Malaria treated in community with ACT <24 hours 5-14y_X" = "maltreat_u24_5_14_com",
     "Malaria treated in community with ACT >24 hours 5-14y_X" = "maltreat_ov24_5_14_com",
     "Malaria treated in community with ACT <24 hours 15+y_X" = "maltreat_u24_ov15_com",
     "Malaria treated in community with ACT >24 hours 15+y_X" = "maltreat_ov24_ov15_com",
     "Malaria treated with ACT <24 hours 0-59m_X" = "maltreat_u24_u5_hf",
     "Malaria treated with ACT >24 hours 0-59m_X" = "maltreat_ov24_u5_hf",
     "Malaria treated with ACT <24 hours 5-14y_X" = "maltreat_u24_5_14_hf",
     "Malaria treated with ACT >24 hours 5-14y_X" = "maltreat_ov24_5_14_hf",
     "Malaria treated with ACT <24 hours 15+y_X" = "maltreat_u24_ov15_hf",
     "Malaria treated with ACT >24 hours 15+y_X" = "maltreat_ov24_ov15_hf"
   )

   # Rename using both mappings
   names(df) <- dplyr::recode(names(df), !!!c(orgunit_rename, column_rename))

   return(df)
 }, error = function(e) {
   message(paste("Error renaming columns:", e))
   return(NULL)
 })
}

# Call function
df <- rename_columns(df)


create_hfid_column <- function(df) {
 df <- df %>%
   group_by(adm1, adm2, adm3, hf) %>%
   mutate(hf_uid = sprintf("hf_%04d", cur_group_id())) %>%
   ungroup()
 return(df)
}

# Load required package
library(dplyr)

# Call function
df <- create_hfid_column(df)
