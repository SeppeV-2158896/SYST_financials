def calculate_reference_income(data):
    """
    Calculate the reference income based on the provided data.
    :param data: A dictionary containing all the required fields.
    :return: The calculated reference income.
    """
    try:
        # Extract fields from the data
        taxable_income = data.get("annual_family_income", 0)
        cadastral_income_rental = data.get("cadastral_income_rental", 0) * 2
        cadastral_income_business = data.get("cadastral_income_business", 0)
        separable_taxable_incomes = data.get("separable_taxable_incomes", 0)
        alimentation_money = data.get("alimentation_money", 0) * 0.8
        living_wages = data.get("living_wages", 0)
        income_replacement_allowance = data.get("income_replacement_allowance", 0)
        foreign_incomes = data.get("foreign_incomes", 0)

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

        return {
            "reference_income": reference_income,
        }
    except Exception as e:
        return {"error": str(e)}