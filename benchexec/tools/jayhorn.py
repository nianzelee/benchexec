"""
BenchExec is a framework for reliable benchmarking.
This file is part of BenchExec.
Copyright (C) 2007-2018  Dirk Beyer
All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

import benchexec.util as util
import benchexec.tools.template
import benchexec.result as result


class Tool(benchexec.tools.template.BaseTool):
    """
    Tool info for JayHorn (https://github.com/jayhorn/jayhorn).
    """

    REQUIRED_PATHS = ["jayhorn.jar", "jayhorn", "libz3.so", "libz3java.so"]

    def executable(self):
        return util.find_executable("jayhorn")

    def version(self, executable):
        return self._version_from_tool(executable)

    def name(self):
        return "JayHorn"

    def cmdline(self, executable, options, tasks, propertyfile, rlimits):
        options = options + ["--propertyfile", propertyfile]
        return [executable] + options + tasks

    def determine_result(self, returncode, returnsignal, output, isTimeout):
        # parse output
        status = result.RESULT_UNKNOWN

        for line in output:
            if "UNSAFE" in line:
                status = result.RESULT_FALSE_PROP
            elif "SAFE" in line:
                status = result.RESULT_TRUE_PROP

        return status
