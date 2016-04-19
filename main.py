#Antony Kwok 108497731
import sys
import tpg

dict = {}
class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """

# These are the nodes of our abstract syntax tree.
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """

    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")


class Array(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        list = []
        for i in self.value:
            list.append(i.evaluate())
        return list

class Str(Node):
    def __init__(self, value):
        self.value = value[1:len(value) - 1]

    def evaluate(self):
        return self.value

class operation(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.op == '[':
            if not (isinstance(right, int)):
                raise SemanticError
            if not (isinstance(left, list) or isinstance(left, str)):
                raise SemanticError
            try:
                return left[right]
            except IndexError:
                raise SemanticError
        elif self.op == "*":
            if not (isinstance(left, int) or isinstance(left, float)) or not (isinstance(right, int) or isinstance(right, float)):
                raise SemanticError
            return left * right

        elif self.op == "/":
            if not (isinstance(left, int) or isinstance(left, float)) or not (isinstance(right, int) or isinstance(right, float)) or right == 0:
                raise SemanticError
            return left / right

        elif self.op == "%":
            if not (isinstance(left, int) or isinstance(left, float)) or not (isinstance(right, int) or isinstance(right, float)):
                raise SemanticError
            return left % right
        elif self.op == "**":
            if not (isinstance(left, int) or isinstance(left, float)) or not (isinstance(right, int) or isinstance(right, float)):
                raise SemanticError
            return pow(left, right)
        elif self.op == "//":
            return left // right
        elif self.op == "+":
            if not ((isinstance(left, int) and isinstance(right, int)) or (
                        isinstance(left, float) and isinstance(right, float)) or
                        (isinstance(left, str) and isinstance(right, str)) or (
                        isinstance(left, list) and isinstance(right, list))):
                raise SemanticError
            return left + right
        elif self.op == "-":
            if not (isinstance(left, int) or isinstance(left, float)) or not (isinstance(right, int) or isinstance(right, float)):
                raise SemanticError
            return left - right
        elif self.op == "in":
            try:
                if (left in right) == True:
                    return 1
                else:
                    return 0
            except:
                raise SemanticError
        elif self.op == "<":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left < right) == True:
                return 1
            else:
                return 0
        elif self.op == "<=":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left <= right) == True:
                return 1
            else:
                return 0
        elif self.op == "==":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left == right) == True:
                return 1
            else:
                return 0
        elif self.op == "<>":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left != right) == True:
                return 1
            else:
                return 0 # !!!fix
        elif self.op == ">":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left > right) == True:
                return 1
            else:
                return 0
        elif self.op == ">=":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left >= right) == True:
                return 1
            else:
                return 0
        elif self.op == "not":
            if not(isinstance(right, int)):
                raise SemanticError
            if right == 0:
                return 1
            else:
                return 0
        elif self.op == "and" or self.op == "&" or self.op == "&&":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if left == 0 or right == 0:
                return 0
            return 1
        elif self.op == "or" or self.op == "|" or self.op == "||":
            if not(isinstance(left, int) and isinstance(right, int)):
                raise SemanticError
            if (left == 0 and right == 0):
                return 0
            return 1

class assignment(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        if isinstance(self.left, Variable):
            dict[self.left.value] = self.right.evaluate()
        elif isinstance(self.left, arrayIndex):
            (self.left.array.evaluate())[self.left.index.evaluate()] = self.right.evaluate()

class Variable(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        try:
            return dict[self.value]
        except:
            raise SemanticError

class arrayIndex(Node):
    """
    A node representing an array[index] call for assignment
    """
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def evaluate(self):
        return self.array

class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

class RealLiteral(Node):
    """
    A node representing real literals.
    """

    def __init__(self, value):
        self.value = float(value)
        print("real is ", value)
    def evaluate(self):
        return self.value

class printer(Node):
    def __init__(self, value):
        self.value = value
    def evaluate(self):
        print(str(self.value.evaluate()))

class block(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        list = []
        for i in self.value:
            list.append(i.evaluate())
        pass

class ifCall(Node):
    def __init__(self, conidition, value):
        self.condition = conidition
        self.value = value

    def evaluate(self):
        if self.condition.evaluate() != 0:
            self.value.evaluate()
        pass

class ifElseCall(Node):
    def __init__(self, ifCall, value):
        self.ifCall = ifCall
        self.value = value

    def evaluate(self):
        if self.ifCall.condition.evaluate() != 0:            #get value of ifCall's condition
            self.ifCall.evaluate()
        else:
            self.value.evaluate()
        pass

class whileLoop(Node):
    def __init__(self, conidition, value):
        self.condition = conidition
        self.value = value

    def evaluate(self):
        while self.condition.evaluate() != 0:
            self.value.evaluate()
        pass

class execute(Node):
    """
    Does evaluate to execute
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        self.value.evaluate()

# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    """

    token var "[A-Za-z][A-Za-z0-9_]*" Variable;
    token real "\d*\.\d*|\.\d*" RealLiteral;
    token int "\d+" IntLiteral;
    token str '\"[^\"]*\"' Str;
    separator space "\s";

    START/a -> ((exe/a)                                            $a = execute(a)$)+;
    exe/a-> statement/a | conditional/a | block/a | conditional/a;
    statement/a -> assign/a | print/a;
    comparison/a -> boolIN/a ( ("\=\="/op | "<>"/op |"<="/op | "<"/op | ">="/op | ">"/op ) boolIN/b    $a = operation(a, op, b) $ )* ;
    assign/a -> left/a "="/op expression/b "\;"                      $a = assignment(a, op, b) $;
    print/a -> ("print" "\(" expression/a "\)" "\;"   $a = printer(a)$);

    left/a -> arrayIndex/a | var/a;
    arrayIndex/a -> var/a "\[" expression/b "\]"                $a = arrayIndex(a, b)$;
    expression/a -> boolOR/a;
    boolOR/a -> boolAND/a ( ("or"/op | "\|\|"/op | "\|"/op) boolAND/b     $a = operation(a, op, b) $ )* ;
    boolAND/a -> boolNOT/a ( ("and"/op | "&&"/op | "&"/op) boolNOT/b   $a = operation(a, op, b) $ )* ;
    boolNOT/a -> comparison/a | "not"/op expression/b              $a = operation(b, op, b) $ ;
    boolIN/a -> xor/a ( "in"/op xor/b                              $a = operation(a, op, b) $ )* ;
    xor/a -> addsub/a ( "xor"/op addsub/b                          $a = operation(a, op, b) $ )* ;
    addsub/a -> floor/a ( ("\+"/op | "\-"/op) floor/b              $a = operation(a, op, b) $ )* ;
    floor/a -> pow/a ( ("//"/op) pow/b                             $a = operation(a, op, b) $ )* ;
    pow/a -> mod/a ( ("\*\*"/op) mod/b                             $a = operation(a, op, b) $ )* ;
    mod/a -> muldiv/a ( ("%"/op) muldiv/b                          $a = operation(a, op, b) $ )* ;
    muldiv/a -> index/a ( ("\*"/op | "/"/op) index/b               $a = operation(a, op, b) $ )* ;
    index/a -> parens/a ( "\[" expression/b "\]"                   $a = operation(a, '[', b) $ )* ;
    parens/a -> "\(" expression/a "\)" | literal/a;
    literal/a -> array/a | real/a | int/a | str/a | var/a;
    array/a -> "\["          $a = Array([]) $
       expression/b          $a.value.append(b) $
       ( "," expression/b    $a.value.append(b) $)*
       "\]"
        | "\[" "\]"          $a = Array([]) $;
    block/a -> "\{"          $a = block([]) $
       ( exe/b    $a.value.append(b) $)*
       "\}"
        | "\{" "\}"          $a = block([]) $;
    conditional/a -> ifElseCall/a | ifCall/a | whileLoop/a;
    whileLoop/a -> "while" "\(" expression/a "\)" block/b          $a = whileLoop(a, b)$;
    ifElseCall/a -> ifCall/a "else" block/b                        $a = ifElseCall(a, b)$;
    ifCall/a -> "if" "\(" expression/a "\)" block/b                $a = ifCall(a, b)$;
    """


# Make an instance of the parser. This acts like a function.
parse = Parser()

# This is the driver code, that reads in lines, deals with errors, and
# prints the output if no error occurs.

# Open the file containing the input.
try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    f = open("input1.txt", "r")

l = f.read()
try:
    # Try to parse the expression.
    node = parse(l)

    # Try to get a result.
    result = node.evaluate()

# If an exception is thrown, print the appropriate error.
except tpg.Error:
    print("SYNTAX ERROR")
    # Uncomment the next line to re-raise the syntax error,
    # displaying where it occurs. Comment it for submission.
    # raise

except SemanticError:
    print("SEMANTIC ERROR")
    # Uncomment the next line to re-raise the semantic error,
    # displaying where it occurs. Comment it for submission.
    # raise

f.close()
