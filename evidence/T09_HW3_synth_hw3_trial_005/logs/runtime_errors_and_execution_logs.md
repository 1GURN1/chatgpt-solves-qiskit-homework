# Runtime Errors and Execution Logs

---------------------------------------------------------------------------
MissingOptionalLibraryError               Traceback (most recent call last)
/tmp/ipykernel_683/4250744334.py in <cell line: 0>()
     30 
     31 qc = build_deutsch_jozsa_circuit(config)
---> 32 qc.draw("mpl")

5 frames
/usr/local/lib/python3.12/dist-packages/qiskit/utils/lazy_tester.py in require_now(self, feature)
    220         if self:
    221             return
--> 222         raise MissingOptionalLibraryError(
    223             libname=self._name, name=feature, pip_install=self._install, msg=self._msg
    224         )

MissingOptionalLibraryError: "The 'pylatexenc' library is required to use 'MatplotlibDrawer'. You can install it with 'pip install pylatexenc'."

---------------------------------------------------------------------------
NOTE: If your import is failing due to a missing package, you can
manually install dependencies using either !pip or !apt.

To view examples of installing some common dependencies, click the
"Open Examples" button below.
---------------------------------------------------------------------------
