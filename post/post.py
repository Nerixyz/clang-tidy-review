#!/usr/bin/env python3

# clang-tidy review - post comments
# Copyright (c) 2022 Peter Hill
# SPDX-License-Identifier: MIT
# See LICENSE for more information

import argparse
import pprint

from clang_tidy_review import (
    PullRequest,
    load_review,
    post_review,
    load_metadata,
    strip_enclosing_quotes,
)


def main(
    repo: str,
    token: str,
    max_comments: int,
    lgtm_comment_body: str,
    dry_run: bool,
) -> None:
    metadata = load_metadata()
    pull_request = PullRequest(repo, metadata["pr_number"], token)

    review = load_review()
    print(
        "clang-tidy-review generated the following review",
        pprint.pformat(review, width=130),
        flush=True,
    )

    post_review(pull_request, review, max_comments, lgtm_comment_body, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Post a review based on feedback generated by the clang-tidy-review action"
    )

    parser.add_argument("--repo", help="Repo name in form 'owner/repo'")
    parser.add_argument(
        "--max-comments",
        help="Maximum number of comments to post at once",
        type=int,
        default=25,
    )
    parser.add_argument(
        "--lgtm-comment-body",
        help="Message to post on PR if no issues are found. An empty string will post no LGTM comment.",
        type=str,
        default='clang-tidy review says "All clean, LGTM! :+1:"',
    )
    parser.add_argument("--token", help="github auth token")
    parser.add_argument(
        "--dry-run", help="Run and generate review, but don't post", action="store_true"
    )

    args = parser.parse_args()

    main(
        repo=args.repo,
        token=args.token,
        max_comments=args.max_comments,
        lgtm_comment_body=strip_enclosing_quotes(args.lgtm_comment_body),
        dry_run=args.dry_run,
    )
