RENDER=python render_program.py
IMAGES="eyecode2/app/static/img"

between_functions:
	$(RENDER) programs/between_functions.py/helpers.py --header "helpers.py" --height 350 $(IMAGES)/between_functions-helpers.png
	$(RENDER) programs/between_functions.py/main.py --header "main.py" --height 350 $(IMAGES)/between_functions-main.png
	convert $(IMAGES)/between_functions-helpers.png $(IMAGES)/between_functions-main.png -append $(IMAGES)/between_functions.png

render: between_functions
	$(RENDER) programs/between_inline.py $(IMAGES)/between_inline.png
	$(RENDER) programs/basketball_iterative.py $(IMAGES)/basketball_iterative.png
	$(RENDER) programs/basketball_recursive.py $(IMAGES)/basketball_recursive.png
	$(RENDER) programs/counting_done.py $(IMAGES)/counting_done.png
	$(RENDER) programs/counting_other.py $(IMAGES)/counting_other.png
	$(RENDER) programs/order_inorder.py $(IMAGES)/order_inorder.png
	$(RENDER) programs/order_shuffled.py $(IMAGES)/order_shuffled.png
	$(RENDER) programs/overload_numbers.py $(IMAGES)/overload_numbers.png
	$(RENDER) programs/overload_words.py $(IMAGES)/overload_words.png
	$(RENDER) programs/rectangle_long.py $(IMAGES)/rectangle_long.png
	$(RENDER) programs/rectangle_short.py $(IMAGES)/rectangle_short.png
	$(RENDER) programs/scope_justreturn.py $(IMAGES)/scope_justreturn.png
	$(RENDER) programs/scope_noreturn.py $(IMAGES)/scope_noreturn.png
	$(RENDER) programs/scope_return.py $(IMAGES)/scope_return.png
	$(RENDER) programs/whitespace_normal.py $(IMAGES)/whitespace_normal.png
	$(RENDER) programs/whitespace_nospace.py $(IMAGES)/whitespace_nospace.png
