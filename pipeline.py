import os
import pandas as pd
import great_expectations as ge

def run_standout_pipeline(data_path: str):
    print("="*60)
    print("🚀 LAUNCHING PRODUCTION-GRADE FEATURE VALIDATION PIPELINE")
    print("="*60)
    
    # 1. Load the raw data asset using Pandas
    raw_df = pd.read_csv(data_path)
    
    # 2. Convert to a Great Expectations Dataset object
    df = ge.from_pandas(raw_df)
    
    # 3. DEFINE ADVANCED MATHEMATICAL & LOGICAL EXPECTATIONS (RULES)
    
    # Rule 1: 'id' column must exist and have unique values
    df.expect_column_to_exist("id")
    df.expect_column_values_to_be_unique("id")
    
    # Rule 2: 'signup_age' must be an integer between 18 and 100
    df.expect_column_values_to_be_of_type("signup_age", "int64")
    df.expect_column_values_to_be_between("signup_age", min_value=18, max_value=100)
    
    # Rule 3: 'email_address' must not contain missing/null values
    df.expect_column_values_to_not_be_null("email_address")
    
    # Rule 4: 'email_address' must conform to standard email regex patterns
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    df.expect_column_values_to_match_regex("email_address", regex=email_regex)
    
    # Rule 5: 'engagement_score' must be a float value between 0.0 and 100.0
    df.expect_column_values_to_be_between("engagement_score", min_value=0.0, max_value=100.0)
    
    # Rule 6: 'account_status' values must strictly belong to an approved status list
    approved_statuses = ["Active", "Inactive", "Suspended"]
    df.expect_column_values_to_be_in_set("account_status", value_set=approved_statuses)
    
    # 4. RUN VALIDATION SUITE & CAPTURE SUMMARY METRICS
    validation_results = df.validate()
    
    # 5. GENERATE AN EXCEPTIONALLY DETAILED ENGINEERING REPORT
    print("\n📊 PIPELINE VALIDATION EXECUTIVE SUMMARY:")
    print(f"🔹 Total Assertions Evaluated : {validation_results['statistics']['evaluated_expectations']}")
    print(f"🔹 Successful Assertions     : {validation_results['statistics']['successful_expectations']}")
    print(f"🔹 Failed Assertions         : {validation_results['statistics']['failed_expectations']}")
    print(f"🔹 Pipeline Success Status    : {'🟢 PASSED' if validation_results['success'] else '🔴 FAILED'}\n")
    
    print("❌ DETAILED FEATURE CORRUPTION DETECTED:")
    print("-" * 60)
    
    for result in validation_results["results"]:
        if not result["success"]:
            rule_type = result["expectation_config"]["expectation_type"]
            column = result["expectation_config"]["kwargs"].get("column")
            failed_count = result["result"].get("unexpected_count", 0)
            failed_values = result["result"].get("unexpected_list", [])
            
            print(f"⚠️ Feature Failure in Column [{column}]")
            print(f"   -> Broken Constraint: {rule_type}")
            print(f"   -> Corrupted Row Count: {failed_count}")
            print(f"   -> Identified Malicious/Invalid Values: {failed_values}")
            print("-" * 60)

if __name__ == "__main__":
    run_standout_pipeline("dataset.csv")
