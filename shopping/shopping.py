import csv
import sys
import numpy as np
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    """
    d = pandas.read_csv(filename, dtype:{"Administrative" : np.int32, "Administrative_Duration" : np.int32, \
        "Informational" : np.int32, "Informational_Duration" : np.int32, "ProductRelated" : np.int32, "ProductRelated_Duration" : np.int32,\
            "BounceRates"  : np.float64, "ExitRates" : np.float64, "PageValues" np.float64, "SpecialDay" : np.float64, \
                "Month" : np.int32, "OperatingSystems" : np.int32, "Browser" : np.int32, "Region" np.int32, \
                    "TrafficType" : np.int32, "VisitorType" : np.int32, "Weekend" : np.int32, "Revenue" : np.int32})
    
    """
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        evidence = []
        labels = []
        for row in reader:
            evidence_line = []
            for i in range(len(row)):
                if i == 0 or i == 2 or i == 4  or i == 11 or i == 12 or i == 13 or i == 14:
                    evidence_line.append(int(row[i]))
                elif i == 1 or i == 3 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9:
                    evidence_line.append(float(row[i]))
                elif i == 10:
                    datetime_obj = datetime.datetime.strptime(row[i][:3], "%b")
                    evidence_line.append(datetime_obj.month - 1)
                elif i == 15:
                    if row[i] == 'Returning_Visitor':
                        evidence_line.append(1)
                    else:
                        evidence_line.append(0)
                elif i == 16:
                    if row[i] == "TRUE":
                        evidence_line.append(1)
                    else:
                        evidence_line.append(0)
                elif i == 17:
                    if row[i] == "TRUE":
                        labels.append(1)
                    else:
                        labels.append(0)
            evidence.append(evidence_line)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(evidence, labels)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    labels = np.array(labels)
    predictions = np.array(predictions)
    unique, count = np.unique(labels, return_counts=True)
    n_pos = count[unique == 1][0]
    n_neg = count[unique == 0][0]
    correct = labels[labels == predictions]
    unique, count = np.unique(correct, return_counts=True)
    n_cor_pos = count[unique == 1][0]
    n_cor_neg = count[unique == 0][0]
    return (n_cor_pos/n_pos, n_cor_neg/n_neg)


if __name__ == "__main__":
    main()
