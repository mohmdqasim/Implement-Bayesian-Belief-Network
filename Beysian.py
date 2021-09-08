

#You Can Update this Table according to you will
#But When you update this table you have to update the Testing Table Aswell
#So the way Beysian is building the Tree , it will check the nodes according to that


#Table
header = [ "Exercise" , "Diet", "label" ]
rows = [
         [ 0.7        ,  0.25 , "No" ],
         [ 0.7       ,  0.75 , "No"],
         [ 0.3       ,  0.25 , "Yes"],
         [ 0.3       ,  0.75 , "Yes"],       
    ]


#You can Uncomment this Table if you needed then you have to remove the upper one
"""
header = [ "Exercise" , "Diet", "Some Other thing", "label" ]
rows = [
         [ 0.7        ,  0.25 , 0.1, "No" ],
         [ 0.7       ,  0.75 ,0.5, "No"],
         [ 0.3       ,  0.25 ,0.6, "Yes"],
         [ 0.3       ,  0.75 ,0.7, "Yes"],       
    ]
"""








#Some Supportive classes and Functions
def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[ -1 ]
        if label not in counts:
            counts[ label ] = 0
        counts[ label ] += 1
    return counts
def is_numeric(value):
    return isinstance( value , int ) or isinstance( value , float )
class Question:
    def __init__(self , column , value):
        self.column = column
        self.value = value

    def match(self , example):
        val = example[ self.column ]
        if is_numeric( val ):
            return val >= self.value
        else:
            return val == self.value

#This function make particion of the table according to right and wrong Rows
def partition(rows , question):
    true_rows , false_rows = [ ] , [ ]
    for row in rows:
        if question.match( row ):
            true_rows.append( row )
        else:
            false_rows.append( row )
    return true_rows , false_rows

#Gini Function of the Beysian
def gini(rows):
    counts = class_counts( rows )
    impurity = 1
    sum=0
    for lbl in counts:
        prob_of_lbl = counts[ lbl ] / float( len( rows ) )
        sum += prob_of_lbl ** 2
    impurity= 1-sum
    return impurity

#Actual Implementation of Beysian Formula
def info_gain(trues , wrong , current_uncertainty):
    p = float( len( trues ) ) / (len( trues ) + len( wrong ))
    return current_uncertainty - p * gini( trues ) - (1 - p) * gini( wrong )

#This Function Finds the Best Split from the Tree
#Actually here we implementing our Beysian Formulas in this function
#to get best split from the Table to make nodes and tree.
def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini( rows )
    for col in range( len(rows[0])-1 ):
        values = set( [ row[ col ] for row in rows ] )
        for val in values:
            question = Question( col , val )
            true_rows , false_rows = partition( rows , question )
            if len( true_rows ) == 0 or len( false_rows ) == 0:
                continue
            gain = info_gain( true_rows , false_rows , current_uncertainty )
            if gain >= best_gain:
                best_gain , best_question = gain , question
    return best_gain , best_question


class Leaf:
    def __init__(self , rows):
        self.predictions = class_counts( rows )


#Class of Decision Node which is used to Make Decision where to go in Tree
#Objects of these class are used in Tree
class Decision_Node:
    def __init__(self , question , true_branch , false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
    def printtree(self):
        print(self.true_branch)
        print(self.false_branch)


#Actually Function to Build the tree using the Table
#This take Table as input and return the Actual Tree after classification
def build_tree(rows):
    gain , question = find_best_split( rows )
    if gain == 0:
        return Leaf( rows )
    true_rows , false_rows = partition( rows , question )
    true_branch = build_tree( true_rows )
    false_branch = build_tree( false_rows )
    decision=Decision_Node( question , true_branch , false_branch ) 
    return decision


#Classify means it acutally take row and Tree as input and gives the ultimate
    #results from the Tree , like we give [0.5,0.5] for Exercise and Diet
    #and it checks from the tree that where this node satisfies and gives the
    #result for that.
def classify(row , node):
    if isinstance( node , Leaf ):
        return node.predictions
    if node.question.match( row ):
        return classify( row , node.true_branch )
    else:
        return classify( row , node.false_branch )

def predict(counts):
    list=[]
    for lbl in counts.keys():
        list.append(lbl)
    return list


#Building the Beysian Tree using the Table
my_tree = build_tree( rows )


#Testing Row for the upper Table
"""
TestHeader = [ "Exercise" , "Diet", "Some Other thing", "label" ]
TestRow = [
         [ 0.7        ,  0.25 , 0.1],
         [ 0.7       ,  0.75 ,0.5],
         [ 0.3       ,  0.25 ,0.6],
         [ 0.3       ,  0.75 ,0.7],       
    ]
"""



# Testing
TestHeader =["Exercise", "Diet"]
TestRow = [
    [ 0.5,0.5 ] ,
  ]



print("Pridicted Data..!!")
for row in TestRow:
  print("Result By : " , row , " : " ,predict( classify( row , my_tree ) ) )
 