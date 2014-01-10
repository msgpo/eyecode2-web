RENDER=python render_program.py
IMAGES="eyecode2/app/static/img"
WEB_IMAGES="../web/files/assets/img/new-programs"

between_functions:
	$(RENDER) programs/between_functions.py/helpers.py --header "helpers.py" --height 350 $(IMAGES)/between_functions-helpers.png
	$(RENDER) programs/between_functions.py/main.py --header "main.py" --height 350 $(IMAGES)/between_functions-main.png
	convert $(IMAGES)/between_functions-main.png $(IMAGES)/between_functions-helpers.png -append $(IMAGES)/between_functions.png

whitespace_nospace_highlight:
	pygmentize -o $(IMAGES)/whitespace_nospace_highlight.png -O style=tango,font_name=Consolas,font_size=19,line_numbers=False,image_pad=0,line_pad=8 programs/whitespace_nospace.py
	convert $(IMAGES)/whitespace_nospace_highlight.png -background white -extent 670x700 $(IMAGES)/whitespace_nospace_highlight.png

render: between_functions whitespace_nospace_highlight
	$(RENDER) programs/between_inline.py $(IMAGES)/between_inline.png
	$(RENDER) programs/basketball_iterative.py $(IMAGES)/basketball_iterative.png
	$(RENDER) programs/basketball_iterative_flipped.py $(IMAGES)/basketball_iterative_flipped.png
	$(RENDER) programs/basketball_recursive.py $(IMAGES)/basketball_recursive.png
	$(RENDER) programs/boolean_easy.py $(IMAGES)/boolean_easy.png
	$(RENDER) programs/boolean_hard.py $(IMAGES)/boolean_hard.png
	$(RENDER) programs/counting_done.py $(IMAGES)/counting_done.png
	$(RENDER) programs/counting_other.py $(IMAGES)/counting_other.png
	$(RENDER) programs/nanotech_comments.py $(IMAGES)/nanotech_comments.png
	$(RENDER) programs/nanotech_nocomments.py $(IMAGES)/nanotech_nocomments.png
	$(RENDER) programs/order_inorder.py $(IMAGES)/order_inorder.png
	$(RENDER) programs/order_shuffled.py $(IMAGES)/order_shuffled.png
	$(RENDER) programs/order_shuffled.py $(IMAGES)/order_shuffled_colors.png \
		--line_colors "['#87DE87','#87DE87','','#FFE680','#FFE680','','#80BEFF','#80BEFF','','#DE8787','#DE8787','','#DDAFE9','#DDAFE9','#DDAFE9','#DDAFE9','#DDAFE9','#DDAFE9']"
	$(RENDER) programs/overload_numbers.py $(IMAGES)/overload_numbers.png
	$(RENDER) programs/overload_words.py $(IMAGES)/overload_words.png
	$(RENDER) programs/rectangle_long.py $(IMAGES)/rectangle_long.png
	$(RENDER) programs/rectangle_short.py $(IMAGES)/rectangle_short.png
	$(RENDER) programs/scope_justreturn.py $(IMAGES)/scope_justreturn.png
	$(RENDER) programs/scope_noreturn.py $(IMAGES)/scope_noreturn.png
	$(RENDER) programs/scope_return.py $(IMAGES)/scope_return.png
	$(RENDER) programs/whitespace_normal.py $(IMAGES)/whitespace_normal.png
	$(RENDER) programs/whitespace_nospace.py $(IMAGES)/whitespace_nospace.png

output:
	python programs/between_functions.py/main.py > programs/output/between_functions.py.txt
	python programs/between_inline.py > programs/output/between_inline.py.txt
	python programs/basketball_iterative.py > programs/output/basketball_iterative.py.txt
	python programs/basketball_iterative_flipped.py > programs/output/basketball_iterative_flipped.py.txt
	python programs/basketball_recursive.py > programs/output/basketball_recursive.py.txt
	python programs/boolean_easy.py > programs/output/boolean_easy.py.txt
	python programs/boolean_hard.py > programs/output/boolean_hard.py.txt
	python programs/counting_done.py > programs/output/counting_done.py.txt
	python programs/counting_other.py > programs/output/counting_other.py.txt
	python programs/nanotech_comments.py > programs/output/nanotech_comments.py.txt
	python programs/nanotech_nocomments.py > programs/output/nanotech_nocomments.py.txt
	python programs/order_inorder.py > programs/output/order_inorder.py.txt
	python programs/order_shuffled.py > programs/output/order_shuffled.py.txt
	python programs/overload_numbers.py > programs/output/overload_numbers.py.txt
	python programs/overload_words.py > programs/output/overload_words.py.txt
	python programs/rectangle_long.py > programs/output/rectangle_long.py.txt
	python programs/rectangle_short.py > programs/output/rectangle_short.py.txt
	python programs/scope_justreturn.py > programs/output/scope_justreturn.py.txt
	python programs/scope_noreturn.py > programs/output/scope_noreturn.py.txt
	python programs/scope_return.py > programs/output/scope_return.py.txt
	python programs/whitespace_normal.py > programs/output/whitespace_normal.py.txt
	python programs/whitespace_nospace.py > programs/output/whitespace_nospace.py.txt

web-images:
	cp $(IMAGES)/*.png $(WEB_IMAGES)/
	for f in $(WEB_IMAGES)/*.png; do convert $$f -trim +repage $$f; done

test:
	nosetests tests.py
