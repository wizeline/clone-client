"""
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
from abc import ABC, abstractmethod
from typing import Any, List

import spacy

nlp = spacy.load("en_core_web_trf")
patterns = [
    {"label": "ORG", "pattern": "Wizeline"},
    {"label": "PERSON", "pattern": [{"lower": "bismarck"}, {"lower": "lepe"}]},
]
# ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
# ruler.add_patterns(patterns)


class MaskBase(ABC):
    """Abstract class, how to implement new mask"""

    @staticmethod
    @abstractmethod
    async def find(data: str) -> List[Any]:
        """Implement this method

        :param data: Data to mask

        :return: New, masked data, and the loopup table to reconstruct it
        """
        return NotImplemented


class IPMask(MaskBase):
    """IP addresses"""

    @staticmethod
    async def find(data: str) -> List[Any]:
        return re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", data)


class NamesMask(MaskBase):
    """Persons names"""

    @staticmethod
    def _process_nlp(data: str):
        # Directly return the processed doc here
        return nlp(data)

    @staticmethod
    async def find(data: str) -> List[Any]:
        person_list = []

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            from functools import partial

            process_nlp = partial(nlp, data)
            doc = await loop.run_in_executor(pool, process_nlp)

        for entity in doc.ents:
            if entity.label_ == "PERSON":
                person_list.append(str(entity))

        return person_list


class LinkMask(MaskBase):
    """Web links"""

    @staticmethod
    async def find(data: str) -> List[Any]:
        return re.findall(
            r'(?i)((?:https?://|www\d{0,3}[.])?[a-z0-9.\-]+[.](?:(?:international)|(?:construction)|(?:contractors)|(?:enterprises)|(?:photography)|(?:immobilien)|(?:management)|(?:technology)|(?:directory)|(?:education)|(?:equipment)|(?:institute)|(?:marketing)|(?:solutions)|(?:builders)|(?:clothing)|(?:computer)|(?:democrat)|(?:diamonds)|(?:graphics)|(?:holdings)|(?:lighting)|(?:plumbing)|(?:training)|(?:ventures)|(?:academy)|(?:careers)|(?:company)|(?:domains)|(?:florist)|(?:gallery)|(?:guitars)|(?:holiday)|(?:kitchen)|(?:recipes)|(?:shiksha)|(?:singles)|(?:support)|(?:systems)|(?:agency)|(?:berlin)|(?:camera)|(?:center)|(?:coffee)|(?:estate)|(?:kaufen)|(?:luxury)|(?:monash)|(?:museum)|(?:photos)|(?:repair)|(?:social)|(?:tattoo)|(?:travel)|(?:viajes)|(?:voyage)|(?:build)|(?:cheap)|(?:codes)|(?:dance)|(?:email)|(?:glass)|(?:house)|(?:ninja)|(?:photo)|(?:shoes)|(?:solar)|(?:today)|(?:aero)|(?:arpa)|(?:asia)|(?:bike)|(?:buzz)|(?:camp)|(?:club)|(?:coop)|(?:farm)|(?:gift)|(?:guru)|(?:info)|(?:jobs)|(?:kiwi)|(?:land)|(?:limo)|(?:link)|(?:menu)|(?:mobi)|(?:moda)|(?:name)|(?:pics)|(?:pink)|(?:post)|(?:rich)|(?:ruhr)|(?:sexy)|(?:tips)|(?:wang)|(?:wien)|(?:zone)|(?:biz)|(?:cab)|(?:cat)|(?:ceo)|(?:com)|(?:edu)|(?:gov)|(?:int)|(?:mil)|(?:net)|(?:onl)|(?:org)|(?:pro)|(?:red)|(?:tel)|(?:uno)|(?:xxx)|(?:ac)|(?:ad)|(?:ae)|(?:af)|(?:ag)|(?:ai)|(?:al)|(?:am)|(?:an)|(?:ao)|(?:aq)|(?:ar)|(?:as)|(?:at)|(?:au)|(?:aw)|(?:ax)|(?:az)|(?:ba)|(?:bb)|(?:bd)|(?:be)|(?:bf)|(?:bg)|(?:bh)|(?:bi)|(?:bj)|(?:bm)|(?:bn)|(?:bo)|(?:br)|(?:bs)|(?:bt)|(?:bv)|(?:bw)|(?:by)|(?:bz)|(?:ca)|(?:cc)|(?:cd)|(?:cf)|(?:cg)|(?:ch)|(?:ci)|(?:ck)|(?:cl)|(?:cm)|(?:cn)|(?:co)|(?:cr)|(?:cu)|(?:cv)|(?:cw)|(?:cx)|(?:cy)|(?:cz)|(?:de)|(?:dj)|(?:dk)|(?:dm)|(?:do)|(?:dz)|(?:ec)|(?:ee)|(?:eg)|(?:er)|(?:es)|(?:et)|(?:eu)|(?:fi)|(?:fj)|(?:fk)|(?:fm)|(?:fo)|(?:fr)|(?:ga)|(?:gb)|(?:gd)|(?:ge)|(?:gf)|(?:gg)|(?:gh)|(?:gi)|(?:gl)|(?:gm)|(?:gn)|(?:gp)|(?:gq)|(?:gr)|(?:gs)|(?:gt)|(?:gu)|(?:gw)|(?:gy)|(?:hk)|(?:hm)|(?:hn)|(?:hr)|(?:ht)|(?:hu)|(?:id)|(?:ie)|(?:il)|(?:im)|(?:in)|(?:io)|(?:iq)|(?:ir)|(?:is)|(?:it)|(?:je)|(?:jm)|(?:jo)|(?:jp)|(?:ke)|(?:kg)|(?:kh)|(?:ki)|(?:km)|(?:kn)|(?:kp)|(?:kr)|(?:kw)|(?:ky)|(?:kz)|(?:la)|(?:lb)|(?:lc)|(?:li)|(?:lk)|(?:lr)|(?:ls)|(?:lt)|(?:lu)|(?:lv)|(?:ly)|(?:ma)|(?:mc)|(?:md)|(?:me)|(?:mg)|(?:mh)|(?:mk)|(?:ml)|(?:mm)|(?:mn)|(?:mo)|(?:mp)|(?:mq)|(?:mr)|(?:ms)|(?:mt)|(?:mu)|(?:mv)|(?:mw)|(?:mx)|(?:my)|(?:mz)|(?:na)|(?:nc)|(?:ne)|(?:nf)|(?:ng)|(?:ni)|(?:nl)|(?:no)|(?:np)|(?:nr)|(?:nu)|(?:nz)|(?:om)|(?:pa)|(?:pe)|(?:pf)|(?:pg)|(?:ph)|(?:pk)|(?:pl)|(?:pm)|(?:pn)|(?:pr)|(?:ps)|(?:pt)|(?:pw)|(?:py)|(?:qa)|(?:re)|(?:ro)|(?:rs)|(?:ru)|(?:rw)|(?:sa)|(?:sb)|(?:sc)|(?:sd)|(?:se)|(?:sg)|(?:sh)|(?:si)|(?:sj)|(?:sk)|(?:sl)|(?:sm)|(?:sn)|(?:so)|(?:sr)|(?:st)|(?:su)|(?:sv)|(?:sx)|(?:sy)|(?:sz)|(?:tc)|(?:td)|(?:tf)|(?:tg)|(?:th)|(?:tj)|(?:tk)|(?:tl)|(?:tm)|(?:tn)|(?:to)|(?:tp)|(?:tr)|(?:tt)|(?:tv)|(?:tw)|(?:tz)|(?:ua)|(?:ug)|(?:uk)|(?:us)|(?:uy)|(?:uz)|(?:va)|(?:vc)|(?:ve)|(?:vg)|(?:vi)|(?:vn)|(?:vu)|(?:wf)|(?:ws)|(?:ye)|(?:yt)|(?:za)|(?:zm)|(?:zw))(?:/[^\s()<>]+[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])?)',
            data,
        )


class PhoneMask(MaskBase):
    """Phone numbers"""

    @staticmethod
    async def find(data: str) -> List[Any]:
        return re.findall(
            r"""((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))""",
            data,
        )


class EmailMask(MaskBase):
    """Email addresses"""

    @staticmethod
    async def find(data: str) -> List[Any]:
        return re.findall(
            r"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",
            data,
        )


class CreditCardMask(MaskBase):
    """Credit Card"""

    @staticmethod
    async def find(data: str) -> List[Any]:
        return re.findall(r"\b(?:\d{4}-){3}\d{4}|\b\d{16}\b", data)


class CustomList(MaskBase):
    """Custom List to mask"""

    @staticmethod
    def _process_nlp(data: str):
        # This is the synchronous part that needs to run in a thread
        return nlp(data)

    @staticmethod
    async def find(data: str) -> List[Any]:
        predefined_words = ["Amazon", "HP", "Disney", "Apple", "Google", "Wizeline"]
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            # Prepare and run the NLP processing in the thread pool
            from functools import partial

            process_nlp = partial(CustomList._process_nlp, data)
            doc = await loop.run_in_executor(pool, process_nlp)

        # Now doc is fully processed, filter the tokens
        return [token.text for token in doc if token.text in predefined_words]
