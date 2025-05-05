from app.models import IncomeThreshold

def calculate_reference_income(data):
    """
    Calculate the reference income based on the provided data.
    :param data: A dictionary containing all the required fields.
    :return: The calculated reference income.
    """
    try:
        # Extract fields from the data
        taxable_income = float(data.get("annual_family_income", 0) or 0.0)
        cadastral_income_rental = float(data.get("cadastral_income_rental", 0) or 0.0) * 2
        cadastral_income_business = float(data.get("cadastral_income_business", 0) or 0.0)
        separable_taxable_incomes = float(data.get("separable_taxable_incomes", 0) or 0.0)
        alimentation_money = float(data.get("alimentation_money", 0) or 0.0) * 0.8
        living_wages = float(data.get("living_wages", 0) or 0.0)
        income_replacement_allowance = float(data.get("income_replacement_allowance", 0) or 0.0)
        foreign_incomes = float(data.get("foreign_incomes", 0) or 0.0)


        # Calculate the reference income
        reference_income = (
            taxable_income
            + cadastral_income_rental
            + cadastral_income_business
            + separable_taxable_incomes
            + alimentation_money
            + living_wages
            + income_replacement_allowance
            + foreign_incomes
        )
        
        print(f"Input data: {data}")
        print(f"Calculated reference income: {reference_income}")

        return {
            "reference_income": reference_income,
        }
    except Exception as e:
        return {"error": str(e)}

def determine_category(living_unit_points, reference_income):
    """
    Determine the category based on living unit points and reference income.

    :param living_unit_points: The living unit points to look up.
    :param reference_income: The calculated reference income.
    :return: A dictionary containing the category and max income thresholds.
    """
    try:
        # Find the matching row in the IncomeThreshold table
        threshold = IncomeThreshold.objects.get(punten_leefeenheid=living_unit_points)
        
        # Check if the reference income is within the min and max range
        if threshold.min_inkomensgrens <= reference_income <= threshold.categorie_4:
            # Determine the category
            if reference_income <= threshold.categorie_1:
                category = 1
            elif reference_income <= threshold.categorie_2:
                category = 2
            elif reference_income <= threshold.categorie_3:
                category = 3
            elif reference_income <= threshold.categorie_4:
                category = 4
            else:
                category = None

            # Return the category and max income thresholds
            return {
                "category": category,
                "max_income_thresholds": {
                    "categorie_1": threshold.categorie_1,
                    "categorie_2": threshold.categorie_2,
                    "categorie_3": threshold.categorie_3,
                    "categorie_4": threshold.categorie_4,
                }
            }
        return None  # No matching category
    except IncomeThreshold.DoesNotExist:
        return None  # No matching row found