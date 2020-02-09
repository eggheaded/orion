def _rca_division(val1, val2, val3, val4):
    """Multi-step division."""
    return (val1 / val2) / (val3 / val4)


def calculate_rca_by_sum(data, entity_column, commodity, value):
    """Groups a dataframe by entity (country or institution) and
       calculates the Revealed Comparative Advantage (RCA) for each 
       entity, based on a commodity. The value used for measurement is
       usually citations and it's done on an annual basis.

    Args:
        data (:code:`pandas.DataFrame`): DF with the re
        entity_column (str): Label of the column containing countries or institutions.
        commodity (str): The Field of Study to measure RCA for.
        value (str): Label of the column containing the values to use for measurement.

    Returns:
        (:code:`pandas.DataFrame`): grouped dataframe with entity, year and calculated RCA.

    """
    entity_sum_topic = (
        data[(data.field_of_study_id == commodity)]
        .groupby([entity_column, "year"])[value]
        .sum()
    )
    entity_sum_all = data.groupby([entity_column, "year"])[value].sum()

    world_sum_topic = (
        data[data.field_of_study_id == commodity].groupby("year")[value].sum()
    )
    world_sum_all = data.groupby("year")[value].sum()

    rca = _rca_division(
        entity_sum_topic, entity_sum_all, world_sum_topic, world_sum_all
    )

    return rca.dropna()


def calculate_rca_by_count(data, entity_column, commodity):
    """Groups a dataframe by entity (country or institution) and
       calculates the Revealed Comparative Advantage (RCA) for each 
       entity, based on a commodity. The value used for measurement is publication 
       volume and it's done on an annual basis.

    Args:
        data (:code:`pandas.DataFrame`): DF with the re
        entity_column (str): Label of the column containing countries or institutions.
        commodity (str): The Field of Study to measure RCA for.

    Returns:
        (:code:`pandas.DataFrame`): grouped dataframe with entity, year and calculated RCA.
    
    """
    entity_count_topic = (
        data[(data.field_of_study_id == commodity)]
        .groupby([entity_column, "year"])["paper_id"]
        .count()
    )
    entity_count_all = data.groupby([entity_column, "year"])["paper_id"].count()

    world_count_topic = (
        data[data.field_of_study_id == commodity].groupby("year")["paper_id"].count()
    )
    world_count_all = data.groupby("year")["paper_id"].count()

    rca = _rca_division(
        entity_count_topic, entity_count_all, world_count_topic, world_count_all
    )

    return rca.dropna()