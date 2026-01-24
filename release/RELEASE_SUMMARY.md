This beta release validates the new tag-detection logic so release jobs run
consistently on tag pushes. It should ensure validation and publishing steps
execute reliably after the CI/CD optimization changes.

We are also continuing to harden the release workflow with clearer abort and
retry behaviors, keeping beta releases safe to repeat while we verify the
end-to-end process.
