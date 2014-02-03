AC_INIT([sinz], 0.1)
AM_INIT_AUTOMAKE
AC_PATH_PROG(PYTHON, python, none)
if test "x$PYTHON" = "xnone"; then
  AC_ERROR(python interpreter required)
fi

AC_CONFIG_FILES(
Makefile
src/Makefile
)
AC_OUTPUT
