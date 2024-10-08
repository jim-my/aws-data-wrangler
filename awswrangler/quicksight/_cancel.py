"""Amazon QuickSight Cancel Module."""

from __future__ import annotations

import logging
from typing import cast

import boto3

from awswrangler import _utils, exceptions, sts
from awswrangler.quicksight._get_list import get_dataset_id

_logger: logging.Logger = logging.getLogger(__name__)


def cancel_ingestion(
    ingestion_id: str,
    dataset_name: str | None = None,
    dataset_id: str | None = None,
    account_id: str | None = None,
    boto3_session: boto3.Session | None = None,
) -> None:
    """Cancel an ongoing ingestion of data into SPICE.

    Note
    ----
    You must pass a not None value for ``dataset_name`` or ``dataset_id`` argument.

    Parameters
    ----------
    ingestion_id
        Ingestion ID.
    dataset_name
        Dataset name.
    dataset_id
        Dataset ID.
    account_id
        If None, the account ID will be inferred from your boto3 session.
    boto3_session
        The default boto3 session will be used if **boto3_session** is ``None``.

    Examples
    --------
    >>> import awswrangler as wr
    >>>  wr.quicksight.cancel_ingestion(ingestion_id="...", dataset_name="...")
    """
    if (dataset_name is None) and (dataset_id is None):
        raise exceptions.InvalidArgument("You must pass a not None name or dataset_id argument.")
    if account_id is None:
        account_id = sts.get_account_id(boto3_session=boto3_session)
    if (dataset_id is None) and (dataset_name is not None):
        dataset_id = get_dataset_id(name=dataset_name, account_id=account_id, boto3_session=boto3_session)
    client = _utils.client(service_name="quicksight", session=boto3_session)
    dataset_id = cast(str, dataset_id)
    client.cancel_ingestion(IngestionId=ingestion_id, AwsAccountId=account_id, DataSetId=dataset_id)
