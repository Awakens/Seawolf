import sys
import tpg


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


class List(Node):
    def __init__(self, value):
        print("List")
        if isinstance(value, list):
            self.value = value
        elif str(value)[0] == '"':
            self.value = value[1:len(value) - 1]
        else:
            self.value = int(value)

    def evaluate(self):
        if isinstance(self.value, list):
            r1 = []
            for k in self.value:
                r1.append(k.evaluate())
            return r1
        else:
            return self.value

class Str(Node):
    def __init__(self, value):
        if str(value)[0] == '"':
            self.value = value[1:len(value) - 1]
            print("Str value is " + self.value)

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
            if not (isinstance(left, int) | isinstance(left, float) | isinstance(right, int) | isinstance(right, float)):
                raise SemanticError
            try:
                return left * right
            except:
                raise SemanticError

        elif self.op == "/":
            if (not(isinstance(left, int) | isinstance(left, float) | isinstance(right, int) | isinstance(right, float))) | right == 0:
                raise SemanticError
            try:
                return left / right
            except:
                raise SemanticError
        elif self.op == "%":
            return left % right
        elif self.op == "**":
            return pow(left, right)
        elif self.op == "//":
            return left // right
        elif self.op == "+":
            if not ((isinstance(left, int) & isinstance(right, int)) | (
                        isinstance(left, float) & isinstance(right, float)) |
                        (isinstance(left, str) & isinstance(right, str)) | (
                        isinstance(left, list) & isinstance(right, list))):
                raise SemanticError
            return left + right
        elif self.op == "-":
            if not (isinstance(left, int) | isinstance(left, float) | isinstance(right, int) | isinstance(right, float)):
                raise SemanticError
            return left - right
        elif self.op == "in":
            try:
                return left in right
            except:
                raise SemanticError
        elif self.op == "<":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left < right
        elif self.op == "<=":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left <= right
        elif self.op == "==":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left == right
        elif self.op == "<>":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left > right  # !!!fix
        elif self.op == ">":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left > right
        elif self.op == ">=":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            return left >= right
        elif self.op == "not":
            if not(isinstance(right, int)):
                raise SemanticError
            if right == 0:
                return False
            else:
                return True
        elif self.op == "and":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            if left == 0 | right == 0:
                return 0
            return 1
        elif self.op == "or":
            if not(isinstance(left, int) & isinstance(right, int)):
                raise SemanticError
            if (left == 0 & right == 0):
                return 0
            return 1


class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        print("intlit is ",value)
        self.value = int(value)

    def evaluate(self):
        return self.value


class RealLiteral(Node):
    """
    A node representing real literals.
    """

    def __init__(self, value):
        print("real")
        self.value = float(value)

    def evaluate(self):
        return self.value


# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    """

    token real "\d*\.\d*|\.\d*" RealLiteral;
    token int "\d+" IntLiteral;
    token str '\"[^\"]*\"' Str;
    separator space "\s";

    START/a -> expression/a;

    expression/a -> boolOR/a;
    boolOR/a -> boolAND/a ( "or"/op boolAND/b                      $a = operation(a, op, b) $ )* ;
    boolAND/a -> boolNOT/a ( "and"/op boolNOT/b                    $a = operation(a, op, b) $ )* ;
    boolNOT/a -> comparison/a | "not"/op expression/b              $a = operation(b, op, b) $ ;
    comparison/a -> boolIN/a ( ("<>"/op |"<="/op | "<"/op | "=="/op | ">="/op | ">"/op ) boolIN/b    $a = operation(a, op, b) $ )* ;
    boolIN/a -> xor/a ( "in"/op xor/b                              $a = operation(a, op, b) $ )* ;
    xor/a -> addsub/a ( "xor"/op addsub/b                          $a = operation(a, op, b) $ )* ;
    addsub/a -> floor/a ( ("\+"/op | "\-"/op) floor/b            $a = operation(a, op, b) $ )* ;
    floor/a -> pow/a ( ("//"/op) pow/b                     $a = operation(a, op, b) $ )* ;
    pow/a -> mod/a ( ("\*\*"/op) mod/b                     $a = operation(a, op, b) $ )* ;
    mod/a -> muldiv/a ( ("%"/op) muldiv/b                     $a = operation(a, op, b) $ )* ;
    muldiv/a -> listIndex/a ( ("\*"/op | "/"/op) listIndex/b              $a = operation(a, op, b) $ )* ;
    listIndex/a -> parens/a ( "\[" expression/b "\]"         $a = operation(a, '[', b) $ )* ;
    parens/a -> "\(" expression/a "\)" | literal/a;
    literal/a -> list/a | real/a | int/a | str/a;
    list/a -> "\["          $a = List([]) $
       expression/b          $a.value.append(b) $
       ( "," expression/b    $a.value.append(b) $)*
       "\]"
        | "\[" "\]"          $a = Value([]) $;
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

# For each line in f
for l in f:
    try:
        # Try to parse the expression.
        node = parse(l)

        # Try to get a result.
        result = node.evaluate()

        # Print the representation of the result.
        print(repr(result))

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