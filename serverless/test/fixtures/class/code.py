#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import math


class Bar:
    static_var = "static Variable"

    def __init__(self, a="a", b="b") -> None:
        self.a = a
        self.b = b
        self.four = 4

    def to_string(self) -> str:
        return f"{self.a}, {self.b}"

    def root(self) -> float:
        return math.sqrt(self.four)


class Foo:
    def __init__(self) -> None:
        self.bar2: Bar = Bar("c", "d")
        self.bar: Bar = Bar()

    def to_string(self) -> str:
        return f"{self.bar.to_string()}, {self.bar2.to_string()}"


foo = Foo()


def print_foo():
    print(foo.to_string())


print_foo()
foo.bar.static_var = "p"
print(str(foo.bar2.static_var))
result = str(foo.bar.root())
