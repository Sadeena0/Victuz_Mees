from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score
import pandas as pd


def forward_selection(model, df, outcome, remaining_predictors, current_best_predictors = [], current_best_score = 0,
                      is_regression = True):
    print(
        f'\nCurrently best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}\n')

    dict_scores = {}

    for possible_predictor in remaining_predictors:
        print(f'Checking predictor: {possible_predictor}')

        test_predictors = df[current_best_predictors + [possible_predictor]]
        model.fit(test_predictors, outcome)

        if is_regression:
            r2 = model.score(test_predictors, outcome)
            n, p = df.shape[0], test_predictors.shape[1]
            score = 1 - (((1 - r2) * (n - 1)) / (n - p - 1))
        else:
            score = f1_score(outcome, model.predict(test_predictors))

        dict_scores[possible_predictor] = score
        print(f'Score: {score}')

    highest_predictor = max(dict_scores, key = dict_scores.get)
    highest_value = dict_scores[highest_predictor]

    if highest_value > current_best_score:
        print(f'Found score higher than current best (Adding {highest_predictor}, score: {highest_value})')
        current_best_predictors, current_best_score = current_best_predictors + [highest_predictor], highest_value

        print(f'Best predictors is now: {current_best_predictors}')

        print(f'Score was improved, recurring...')
        return forward_selection(model, df, outcome, list(set(remaining_predictors) - {highest_predictor}),
                                 current_best_predictors,
                                 current_best_score, is_regression)

    print(f'Best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}')
    return current_best_predictors


def backward_elimination(model, df, outcome, current_best_predictors, current_best_score = 0, is_regression = True):
    print(
        f'\nCurrently best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}')

    dict_scores = {}

    for possible_predictor in current_best_predictors:
        print(f'Checking predictor: {possible_predictor}')

        test_predictors = df[list(set(current_best_predictors) - {possible_predictor})]
        model.fit(test_predictors, outcome)

        if is_regression:
            r2 = model.score(test_predictors, outcome)
            n, p = df.shape[0], test_predictors.shape[1]
            score = 1 - (((1 - r2) * (n - 1)) / (n - p - 1))
        else:
            score = f1_score(outcome, model.predict(test_predictors))

        dict_scores[possible_predictor] = score

        print(f'Score: {score}')

    highest_predictor = max(dict_scores, key = dict_scores.get)
    highest_value = dict_scores[highest_predictor]

    if highest_value >= current_best_score:
        print(f'Found score higher than current best (Removing {highest_predictor}, score: {highest_value})')
        current_best_predictors, current_best_score = list(
            set(current_best_predictors) - {highest_predictor}), highest_value

        print(f'Best predictors is now: {current_best_predictors}')

        print(f'Score was improved, recurring...')
        return backward_elimination(model, df, outcome, current_best_predictors, current_best_score, is_regression)

    print(f'Best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}')
    return current_best_predictors


def selection(model, df, outcome, remaining_predictors, current_best_predictors = [], current_best_score = 0,
              mode = 'forward', metric = 'adj_r2'):
    """Perform stepwise selection (forward or backward) on the given model and dataset.

    Parameters:
    - model: The machine learning model to be trained.
    - df: DataFrame containing the dataset.
    - outcome: DataFrame of the outcome.
    - predictors: List of possible predictors to choose from.
    - current_best_predictors: List of predictors chosen in previous iterations (default empty).
    - current_best_score: Score from the previous iteration (default 0).
    - mode: 'forward' or 'backward' to specify the stepwise method.
    - is_regression: If True, assume it's a regression problem; otherwise, classification.

    Returns:
    - The list of selected predictors and the corresponding score."""

    # print(f'\nCurrently best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}')

    dict_scores = {}

    if len(remaining_predictors) == 0:
        return None, 0

    # For each individual predictor in remaining predictors
    for possible_predictor in remaining_predictors:
        # print(f'Checking predictor: {possible_predictor}')

        # If forward, add it to current best predictors to test score
        if mode == 'forward':
            test_predictors = df[current_best_predictors + [possible_predictor]]
        # If backwards, remove it from current best predictors to test score
        elif mode == 'backward':
            test_predictors = df[list(set(remaining_predictors) - {possible_predictor})]

        model.fit(test_predictors, outcome)

        # Get score
        score = 0
        if metric == 'adj_r2':
            r2 = model.score(test_predictors, outcome)
            n, p = df.shape[0], test_predictors.shape[1]
            score = 1 - (((1 - r2) * (n - 1)) / (n - p - 1))
        elif metric == 'f1':
            score = f1_score(outcome, model.predict(test_predictors))
        elif metric == 'recall' or metric == 'rec':
            score = recall_score(outcome, model.predict(test_predictors))
        elif metric == 'accuracy' or metric == 'acc':
            score = accuracy_score(outcome, model.predict(test_predictors))
        elif metric == 'precision' or metric == 'pre':
            score = precision_score(outcome, model.predict(test_predictors), zero_division = 0)

        dict_scores[possible_predictor] = score
        # print(f'Score: {score}')

    # Get predictor with the highest score
    highest_predictor = max(dict_scores, key = dict_scores.get)
    highest_value = dict_scores[highest_predictor]

    if mode == 'forward':
        if highest_value > current_best_score:
            # print(f'Found score higher than current best (Adding {highest_predictor}, score: {highest_value})')

            # Add the best predictor to current best predictor & update best score
            current_best_predictors, current_best_score = current_best_predictors + [highest_predictor], highest_value
            remaining_predictors = list(set(remaining_predictors) - {highest_predictor})

            # print(f'Best predictors is now: {current_best_predictors}')
            # print(f'Score was improved, recurring...')

            # Recur and remove this iteration's best predictor from remaining predictors to test
            return selection(model, df, outcome, remaining_predictors, current_best_predictors,
                             current_best_score, mode, metric)
    elif mode == 'backward':
        if highest_value >= current_best_score:
            # print(f'Found score higher than current best (Removing {highest_predictor}, score: {highest_value})')

            # Remove the best predictor from remaining predictors & update best score
            remaining_predictors, current_best_score = list(
                set(remaining_predictors) - {highest_predictor}), highest_value
            current_best_predictors = remaining_predictors

            # print(f'Best predictors is now: {current_best_predictors}')
            # print(f'Score was improved, recurring...')

            return selection(model, df, outcome, remaining_predictors, current_best_predictors, current_best_score,
                             mode, metric)

    # print(f'Best predictors: {current_best_predictors}\nCorresponding score: {current_best_score}')
    return current_best_predictors, current_best_score


def merge_on_aanwezigheid(aanwezigheid_df, evenement_df, gebruikers_df):
    # Drop duplicates
    df = aanwezigheid_df.drop_duplicates(subset = ['EvenementID', 'GebruikerID'], keep = 'first')

    # Merge aanwezigheid_df with evenement_df
    df = df.merge(evenement_df, on = "EvenementID", how = "left")

    # Merge the result with gebruikers_df
    df = df.merge(gebruikers_df, on = "GebruikerID", how = "left")

    # Rename columns for consistency
    df.rename(
        columns = {col: f"Evenement_{col}" for col in evenement_df.columns if col != "EvenementID"},
        inplace = True
    )

    df.rename(
        columns = {col: f"Gebruiker_{col}" for col in gebruikers_df.columns if col != "GebruikerID"},
        inplace = True
    )

    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    return df


def merge_on_bericht(bericht_df, evenement_df, gebruikers_df):
    # Merge bericht_df with evenement_df
    df = bericht_df.merge(evenement_df, on = "EvenementID", how = "left")

    # Merge the result with gebruikers_df
    df = df.merge(gebruikers_df, on = "GebruikerID", how = "left")

    # Rename columns for consistency
    df.rename(
        columns = {col: f"Evenement_{col}" for col in evenement_df.columns if col != "EvenementID"},
        inplace = True
    )

    df.rename(
        columns = {col: f"Gebruiker_{col}" for col in gebruikers_df.columns if col != "GebruikerID"},
        inplace = True
    )

    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    return df


def merge_on_all(bericht_df, evenement_df, gebruikers_df, aanwezigheid_df):
    # Drop duplicates
    df = aanwezigheid_df.drop_duplicates(subset = ['EvenementID', 'GebruikerID'], keep = 'first')

    # Merge df with evenement_df
    df = df.merge(evenement_df, on = "EvenementID", how = "left")

    # Merge the result with gebruikers_df
    df = df.merge(gebruikers_df, on = "GebruikerID", how = "left")

    # Merge bericht_df with evenement_df
    df = bericht_df.merge(df, on = ['EvenementID', 'GebruikerID'], how = "left")

    # Rename columns for consistency
    df.rename(
        columns = {col: f"Evenement_{col}" for col in evenement_df.columns if col != "EvenementID"},
        inplace = True
    )

    df.rename(
        columns = {col: f"Gebruiker_{col}" for col in gebruikers_df.columns if col != "GebruikerID"},
        inplace = True
    )

    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    return df
