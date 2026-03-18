funcToClosureCellContent=lambda f:(
  tuple(c.cell_contents for c in f.__closure__)if f.__closure__ else()
)
