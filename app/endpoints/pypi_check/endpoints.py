# -*- coding: utf-8 -*-
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from endpoints.pypi_check import forms
from resources import templates
from starlette_wtf import csrf_protect
from endpoints.pypi_check.pypi_calls import main, process_raw
from endpoints.pypi_check.crud import get_request_group_id

base: str = "pypi"


@csrf_protect
async def pypi_index(request):
    host_ip = request.client.host
    form = await forms.RequirementsForm.from_formdata(request)
    form_data = await request.form()
    if form.validate_on_submit():

        logger.info(form_data["requirements"])
        requirements_str = form_data["requirements"]
        text_in: str = requirements_str

        request_group_id = await main(raw_data=text_in, host_ip=host_ip)

        logger.info("Redirecting user to index page /")
        return RedirectResponse(
            url=f"/pypi/results/{str(request_group_id)}", status_code=303
        )
    status_code = 200
    template = f"/{base}/pypi_new.html"
    context = {"request": request, "form": form}
    logger.info(f"page accessed: /pypi/")
    return templates.TemplateResponse(template, context, status_code=status_code)


async def pypi_result(request):
    
    request_group_id = request.path_params["page"]

    data =  await get_request_group_id(request_group_id=request_group_id)
    
    template = f"/{base}/result.html"
    context = {"request": request, "data": data}
    logger.info(f"page accessed: /pypi/")
    return templates.TemplateResponse(template, context)
